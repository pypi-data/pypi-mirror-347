import os
import pickle
import logging
import re
from intervaltree import IntervalTree  # , Interval
import pandas as pd
from typing import Optional, TypedDict
from ._transcriptome_io import import_ref_transcripts
from .gene import Gene
from ._transcriptome_filter import (
    DEFAULT_GENE_FILTER,
    DEFAULT_TRANSCRIPT_FILTER,
    DEFAULT_REF_TRANSCRIPT_FILTER,
    ANNOTATION_VOCABULARY,
    SPLICE_CATEGORY,
)
from . import __version__

logger = logging.getLogger("isotools")

# as this class has diverse functionality, its split among:
# transcriptome.py (this file- initialization and user level basic functions)
# _transcriptome_io.py (input/output primary data files/tables)
# _transcriptome_stats.py (statistical methods)
# _trnascriptome_plots.py (plots)
# _transcriptome_filter.py (gene/transcript iteration and filtering)


class FilterData(TypedDict):
    gene: dict[str, str]
    transcript: dict[str, str]
    reference: dict[str, str]


class InfosData(TypedDict):
    biases: bool


class Transcriptome:
    """Contains sequencing data and annotation for Long Read Transcriptome Sequencing (LRTS) Experiments."""

    # initialization and save/restore data

    data: dict[str, IntervalTree[Gene]]
    "One IntervalTree of Genes for each chromosome."
    infos: InfosData
    chimeric: dict
    filter: FilterData
    _idx: dict[str, Gene]

    def __init__(
        self,
        data: Optional[dict[str, IntervalTree[Gene]]] = None,
        infos=None,
        chimeric=None,
        filter=None,
    ):
        if infos is None:
            infos = {}
        if chimeric is None:
            chimeric = {}
        if filter is None:
            filter = {}

        """Constructor method"""
        if data is not None:
            self.data = data
            self.infos = infos
            self.chimeric = chimeric
            self.filter = filter
            assert "reference_file" in self.infos
            self.make_index()

    @classmethod
    def from_reference(cls, reference_file: str, file_format="auto", **kwargs):
        """Creates a Transcriptome object by importing reference annotation.

        :param reference_file: Reference file in gff3 format or pickle file to restore previously imported annotation
        :param file_format: Specify the file format of the provided reference_file.
            If set to "auto" the file type is inferred from the extension.
        :param chromosome: If reference file is gtf/gff, restrict import on specified chromosomes
        """

        if file_format == "auto":
            file_format = os.path.splitext(reference_file)[1].lstrip(".")
            if file_format == "gz":
                file_format = os.path.splitext(reference_file[:-3])[1].lstrip(".")
        if file_format in ("gff", "gff3", "gtf"):
            logger.info(
                "importing reference from %s file %s", file_format, reference_file
            )
            transcriptome = cls()
            transcriptome.chimeric = {}
            transcriptome.data = import_ref_transcripts(
                reference_file, transcriptome, file_format, **kwargs
            )
            transcriptome.infos = {
                "reference_file": reference_file,
                "isotools_version": __version__,
            }
            transcriptome.filter = {
                "gene": DEFAULT_GENE_FILTER.copy(),
                "transcript": DEFAULT_TRANSCRIPT_FILTER.copy(),
                "reference": DEFAULT_REF_TRANSCRIPT_FILTER.copy(),
            }
            for subcat in ANNOTATION_VOCABULARY:
                tag = "_".join(re.findall(r"\b\w+\b", subcat)).upper()
                if tag[0].isdigit():
                    tag = "_" + tag
                transcriptome.filter["transcript"][tag] = f'"{subcat}" in annotation[1]'
            for i, cat in enumerate(SPLICE_CATEGORY):
                transcriptome.filter["transcript"][cat] = f"annotation[0]=={i}"

        elif file_format == "pkl":
            # warn if kwargs are specified: kwargs are ignored
            if kwargs:
                logger.warning(
                    "The following parameters are ignored when loading reference from pkl: %s",
                    ", ".join(kwargs),
                )
            transcriptome = cls.load(reference_file)
            if "sample_table" in transcriptome.infos:
                logger.warning(
                    "the pickle file seems to contain sample information... extracting reference"
                )
                transcriptome = transcriptome._extract_reference()
        else:
            raise ValueError(
                "invalid file format %s of file %s" % (file_format, reference_file)
            )
        transcriptome.make_index()
        return transcriptome

    def save(self, pickle_file: str):
        """Saves transcriptome information (including reference) in a pickle file.

        :param pickle_file: Filename to save data"""
        logger.info("saving transcriptome to %s", pickle_file)
        pickle.dump(self, open(pickle_file, "wb"))

    @classmethod
    def load(cls, pickle_file: str):
        """Restores transcriptome information from a pickle file.

        :param pickle_file: Filename to restore data"""

        logger.info("loading transcriptome from %s", pickle_file)
        transcriptome: Transcriptome = pickle.load(open(pickle_file, "rb"))
        pickled_version = transcriptome.infos.get("isotools_version", "<0.2.6")
        if pickled_version != __version__:
            logger.warning(
                "This is isotools version %s, but data has been pickled with version %s, which may be incompatible",
                __version__,
                pickled_version,
            )
        transcriptome.make_index()
        return transcriptome

    def save_reference(self, pickle_file=None):
        """Saves the reference information of a transcriptome in a pickle file.

        :param pickle_file: Filename to save data"""
        if pickle_file is None:
            pickle_file = self.infos["reference_file"] + ".isotools.pkl"
        logger.info("saving reference to %s", pickle_file)
        ref_tr = self._extract_reference()
        pickle.dump(ref_tr, open(pickle_file, "wb"))

    def _extract_reference(self):
        if not "sample_table" not in self.infos:
            return self  # only reference info - assume that self.data only contains reference data
        # make a new transcriptome
        ref_info = {
            k: v
            for k, v in self.infos.items()
            if k in ["reference_file", "isotools_version"]
        }
        ref_transcriptome = type(self)(data={}, infos=ref_info, filter=self.filter)
        # extract the reference genes and link them to the new ref_tr
        keep = {
            "ID",
            "chr",
            "strand",
            "name",
            "reference",
        }  # no coverage, segment_graph, transcripts
        for chrom, tree in self.data.items():
            ref_transcriptome.data[chrom] = IntervalTree(
                Gene(
                    gene.start,
                    gene.end,
                    {k: v for k, v in gene.data.items() if k in keep},
                    ref_transcriptome,
                )
                for gene in tree
                if gene.is_annotated
            )
        ref_transcriptome.make_index()
        return ref_transcriptome

    def make_index(self):
        """Updates the index of gene names and ids (e.g. used by the the [] operator)."""
        idx = dict()
        for gene in self:
            if gene.id in idx:  # at least id should be unique - maybe raise exception?
                logger.warning(
                    "%s seems to be ambigous: %s vs %s",
                    gene.id,
                    str(idx[gene.id]),
                    str(gene),
                )
            idx[gene.name] = gene
            idx[gene.id] = gene
        self._idx = idx

    # basic user level functionality
    def __getitem__(self, key):
        """
        Syntax: self[key]

        :param key: May either be the gene name or the gene id
        :return: The gene specified by key."""
        return self._idx[key]

    def __len__(self):
        """Syntax: len(self)

        :return: The number of genes."""
        return self.n_genes

    def __contains__(self, key):
        """Syntax: key in self

        Checks whether key is in self.

        :param key: May either be the gene name or the gene id"""
        return key in self._idx

    def remove_chromosome(self, chromosome):
        """Deletes the chromosome from the transcriptome

        :param chromosome: Name of the chromosome to remove"""
        del self.data[chromosome]
        self.make_index()

    def _get_sample_idx(self, name_column="name"):
        "a dict with group names as keys and index lists as values"
        return {sample: i for i, sample in enumerate(self.sample_table[name_column])}

    @property
    def sample_table(self):
        """The sample table contains sample names, group information, long read coverage, as well as all other potentially
        relevant information on the samples."""
        try:
            return self.infos["sample_table"]
        except KeyError:
            return pd.DataFrame(
                columns=[
                    "name",
                    "file",
                    "group",
                    "nonchimeric_reads",
                    "chimeric_reads",
                ],
                dtype="object",
            )

    @property
    def samples(self) -> list:
        """An ordered list of sample names."""
        return list(self.sample_table.name)

    def groups(self, by="group") -> dict:
        """Get sample groups as defined in columns of the sample table.

        :param by: A column name of the sample table that defines the grouping.
        :return: Dict with groupnames as keys and list of sample names as values.
        """
        return dict(self.sample_table.groupby(by)["name"].apply(list))

    @property
    def n_transcripts(self) -> int:
        """The total number of transcripts isoforms."""
        if self.data is None:
            return 0
        return sum(gene.n_transcripts for gene in self)

    @property
    def n_genes(self) -> int:
        """The total number of genes."""
        if self.data is None:
            return 0
        return sum((len(t) for t in self.data.values()))

    @property
    def novel_genes(self) -> int:  # this is used for id assignment
        """The total number of novel (not reference) genes."""
        try:
            return self.infos["novel_counter"]
        except KeyError:
            self.infos["novel_counter"] = 0
            return 0

    @property
    def chromosomes(self) -> list:
        """The list of chromosome names."""
        return list(self.data)

    def _add_novel_gene(
        self, chrom, start, end, strand, info, novel_prefix="IT_novel_"
    ):
        n_novel = self.novel_genes
        info.update(
            {"chr": chrom, "ID": f"{novel_prefix}{n_novel+1:05d}", "strand": strand}
        )
        g = Gene(start, end, info, self)
        self.data.setdefault(chrom, IntervalTree()).add(g)
        self.infos["novel_counter"] += 1
        return g

    def __str__(self):
        return "{} object with {} genes and {} transcripts".format(
            type(self).__name__, self.n_genes, self.n_transcripts
        )

    def __repr__(self):
        return object.__repr__(self)

    def __iter__(self):
        return (gene for tree in self.data.values() for gene in tree)

    # IO: load new data from primary data files
    from ._transcriptome_io import (
        add_sample_from_bam,
        add_sample_from_csv,
        remove_samples,
        add_short_read_coverage,
        remove_short_read_coverage,
        collapse_immune_genes,
    )

    # IO: output data as tables or other human readable format
    from ._transcriptome_io import (
        gene_table,
        transcript_table,
        chimeric_table,
        write_gtf,
        write_fasta,
        export_alternative_splicing,
        import_sqanti_classification,
        export_end_sequences,
    )

    # filtering functionality and iterators
    from ._transcriptome_filter import (
        add_qc_metrics,
        add_orf_prediction,
        add_filter,
        remove_filter,
        iter_genes,
        iter_transcripts,
        iter_ref_transcripts,
    )

    # statistic: differential splicing, alternative_splicing_events
    from ._transcriptome_stats import (
        die_test,
        altsplice_test,
        coordination_test,
        alternative_splicing_events,
        rarefaction,
    )

    # statistic: summary tables (can be used as input to plot_bar / plot_dist)
    from ._transcriptome_stats import (
        altsplice_stats,
        filter_stats,
        transcript_length_hist,
        transcript_coverage_hist,
        transcripts_per_gene_hist,
        exons_per_transcript_hist,
        downstream_a_hist,
        direct_repeat_hist,
        entropy_calculation,
        str_var_calculation,
    )

    # protein domain annotation
    from .domains import add_hmmer_domains, add_annotation_domains
