"""Manages methods to write a summary file.

Copyright (c) 2022 to present Mitja Maximilian Zdouc, PhD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import logging
from pathlib import Path
from typing import Self

from pydantic import BaseModel

from fermo_core.input_output.class_parameter_manager import ParameterManager

logger = logging.getLogger("fermo_core")


class SummaryWriter(BaseModel):
    """Pydantic-based blass to manage methods to write a textual process summary.

    Attributes:
        params: a ParameterClass instance
        destination: the place to write the log to
        summary: the summary to write out.
    """

    params: ParameterManager
    destination: Path
    summary: list = []

    def write_summary(self: Self):
        """Write the summary to the specified destination."""
        with open(self.destination, "w") as outfile:
            outfile.write("\n".join(self.summary))

    def summarize_peaktableparameters(self: Self):
        if self.params.PeaktableParameters is not None:
            self.summary.append(
                f"Molecular feature and sample information was parsed from the file "
                f"'{self.params.PeaktableParameters.filepath.name}' in the format "
                f"'{self.params.PeaktableParameters.format}' with "
                f"'{self.params.PeaktableParameters.polarity}' ion mode polarity."
            )

    def summarize_msmsparameters(self: Self):
        if self.params.MsmsParameters is not None:
            self.summary.append(
                f"MS/MS fragmentation information was parsed from the file "
                f"'{self.params.MsmsParameters.filepath.name}' in the format "
                f"'{self.params.MsmsParameters.format}'. "
                f"MS/MS fragments +- 10 mass units around precursor m/z were removed."
            )
            if self.params.MsmsParameters.rel_int_from > 0:
                self.summary.append(
                    f"MS/MS fragments with an intensity less than "
                    f"'{self.params.MsmsParameters.rel_int_from}' relative to the "
                    f"base peak were removed."
                )

    def summarize_phenotypeparameters(self: Self):
        if self.params.PhenotypeParameters is not None:
            self.summary.append(
                f"Phenotype/bioactivity information was parsed from the file "
                f"'{self.params.PhenotypeParameters.filepath.name}' in the format "
                f"'{self.params.PhenotypeParameters.format}'."
            )

    def summarize_groupmetadataparameters(self: Self):
        if self.params.GroupMetadataParameters is not None:
            self.summary.append(
                f"Group metadata information was parsed from the file "
                f"'{self.params.GroupMetadataParameters.filepath.name}' "
                f"in the format '{self.params.GroupMetadataParameters.format}'."
            )

    def summarize_speclibparameters(self: Self):
        if self.params.SpecLibParameters is not None:
            self.summary.append(
                f"A user-specified spectral library was parsed from the file "
                f"'{self.params.SpecLibParameters.dirpath.name}' "
                f"in the format '{self.params.SpecLibParameters.format}'."
            )

    def summarize_ms2queryresultsparameters(self: Self):
        if self.params.MS2QueryResultsParameters is not None:
            self.summary.append(
                f"MS2Query results were parsed from the file "
                f"'{self.params.MS2QueryResultsParameters.filepath.name}'. "
                f"Only results with a score above a user-specified value of "
                f"'{self.params.MS2QueryResultsParameters.score_cutoff}' were retained."
            )

    def summarize_asresultsparameters(self: Self):
        if self.params.AsResultsParameters is not None:
            self.summary.append(
                f"antiSMASH results were parsed from the directory "
                f"'{self.params.AsResultsParameters.directory_path.name}'. "
                f"KnownClusterBlast matches were only retained if they were above a "
                f"user-specified similarity cutoff of "
                f"'{self.params.AsResultsParameters.similarity_cutoff}'."
            )

    def summarize_featurefilteringparameters(self: Self):
        if not (
            self.params.FeatureFilteringParameters
            and self.params.FeatureFilteringParameters.activate_module
        ):
            return

        if (
            self.params.FeatureFilteringParameters.activate_module
            and self.params.FeatureFilteringParameters.module_passed
        ):
            self.summary.append(
                f"Molecular features were filtered and only retained if they were "
                f"inside the relative intensity(height) range of "
                f"'{self.params.FeatureFilteringParameters.filter_rel_int_range_min}"
                f"-"
                f"{self.params.FeatureFilteringParameters.filter_rel_int_range_max}'"
                f" in at least one sample (relative to the feature with the "
                f"highest intensity(height) in the sample)."
            )
            self.summary.append(
                f"Molecular features were filtered and only retained if they were "
                f"inside the relative area range of "
                f"'{self.params.FeatureFilteringParameters.filter_rel_area_range_min}"
                f"-"
                f"{self.params.FeatureFilteringParameters.filter_rel_area_range_max}'"
                f" in at least one sample (relative to the feature with the "
                f"highest area in the sample)."
            )
        else:
            self.summary.append(
                f"During filtering of molecular features, an error occurred, and the "
                f"module terminated prematurely. For more information, see the logs."
            )

    def summarize_adductannotationparameters(self: Self):
        if not (
            self.params.AdductAnnotationParameters
            and self.params.AdductAnnotationParameters.activate_module
        ):
            return

        if (
            self.params.AdductAnnotationParameters.activate_module
            and self.params.AdductAnnotationParameters.module_passed
        ):
            self.summary.append(
                f"For each sample, overlapping molecular features were annotated for "
                f"ion adducts using a cutoff mass deviation value of "
                f"'{self.params.AdductAnnotationParameters.mass_dev_ppm}' ppm."
            )
        else:
            self.summary.append(
                f"During adduct annotation, an error occurred, and the "
                f"module terminated prematurely. For more information, see the logs."
            )

    def summarize_neutrallossparameters(self: Self):
        if not (
            self.params.NeutralLossParameters
            and self.params.NeutralLossParameters.activate_module
        ):
            return

        if (
            self.params.NeutralLossParameters.activate_module
            and self.params.NeutralLossParameters.module_passed
        ):
            self.summary.append(
                f"For each molecular feature, neutral losses were calculated between "
                f"the precursor m/z and each MS/MS fragment peak m/z and matched "
                f"against a "
                f"library of annotated neutral losses, using a cutoff mass deviation "
                f"value of '{self.params.NeutralLossParameters.mass_dev_ppm}' ppm."
            )
        else:
            self.summary.append(
                f"During neutral loss annotation, an error occurred, and the "
                f"module terminated prematurely. For more information, see the logs."
            )

    def summarize_fragmentannparameters(self: Self):
        if not (
            self.params.FragmentAnnParameters
            and self.params.FragmentAnnParameters.activate_module
        ):
            return

        if (
            self.params.FragmentAnnParameters.activate_module
            and self.params.FragmentAnnParameters.module_passed
        ):
            self.summary.append(
                f"For each molecular feature, MS/MS fragments were matched against a "
                f"library of annotated MS/MS fragments, using a cutoff mass deviation "
                f"value of '{self.params.FragmentAnnParameters.mass_dev_ppm}' ppm."
            )
        else:
            self.summary.append(
                f"During fragment annotation, an error occurred, and the "
                f"module terminated prematurely. For more information, see the logs."
            )

    def summarize_specsimnetworkcosineparameters(self: Self):
        if not (
            self.params.SpecSimNetworkCosineParameters
            and self.params.SpecSimNetworkCosineParameters.activate_module
        ):
            return

        if (
            self.params.SpecSimNetworkCosineParameters.activate_module
            and self.params.SpecSimNetworkCosineParameters.module_passed
        ):
            self.summary.append(
                f"MS/MS spectra of all molecular features with more than '"
                f"{self.params.SpecSimNetworkCosineParameters.msms_min_frag_nr}' "
                f"fragment ions were compared pairwise and "
                f"scored using the 'modified cosine' algorithm, with a fragment "
                f"tolerance of "
                f"'{self.params.SpecSimNetworkCosineParameters.fragment_tol}'. "
                f"From the resulting similarity matrix, a network was created, "
                f"with features represented as nodes and the similarity value as "
                f"edges. Edges were pruned if their score was below a similarity "
                f"cutoff of '"
                f"{self.params.SpecSimNetworkCosineParameters.score_cutoff}'. "
                f"Also, edges were pruned so that only the '"
                f"{self.params.SpecSimNetworkCosineParameters.max_nr_links}' highest "
                f"scoring edges remained."
            )
        else:
            self.summary.append(
                f"During spectral similarity networking calculation using the "
                f"modified cosine algorithm, an error occurred, and the "
                f"module terminated prematurely. For more information, see the logs."
            )

    def summarize_specsimnetworkdeepscoreparameters(self: Self):
        if not (
            self.params.SpecSimNetworkDeepscoreParameters
            and self.params.SpecSimNetworkDeepscoreParameters.activate_module
        ):
            return

        if (
            self.params.SpecSimNetworkDeepscoreParameters.activate_module
            and self.params.SpecSimNetworkDeepscoreParameters.module_passed
        ):
            self.summary.append(
                f"MS/MS spectra of all molecular features with more than '"
                f"{self.params.SpecSimNetworkDeepscoreParameters.msms_min_frag_nr}' "
                f"fragment ions were compared pairwise and "
                f"scored using the 'MS2Deepscore' algorithm. "
                f"From the resulting similarity matrix, a network was created, "
                f"with features represented as nodes and the similarity value as "
                f"edges. Edges were pruned if their score was below a similarity "
                f"cutoff of '"
                f"{self.params.SpecSimNetworkDeepscoreParameters.score_cutoff}'. "
                f"Also, edges were pruned so that only the '"
                f"{self.params.SpecSimNetworkDeepscoreParameters.max_nr_links}' highest"
                f" scoring edges remained."
            )
        else:
            self.summary.append(
                f"During spectral similarity networking calculation using the "
                f"MS2DeepScore algorithm, an error occurred, and the "
                f"module terminated prematurely. For more information, see the logs."
            )

    def summarize_blankassignmentparameters(self: Self):
        if not (
            self.params.BlankAssignmentParameters
            and self.params.BlankAssignmentParameters.activate_module
        ):
            return

        if (
            self.params.BlankAssignmentParameters.activate_module
            and self.params.BlankAssignmentParameters.module_passed
        ):
            self.summary.append(
                f"Molecular features only detected in sample-blanks were considered "
                f"blank-associated, as were features that had a quotient of less than "
                f"'{self.params.BlankAssignmentParameters.factor}' when their "
                f"'{self.params.BlankAssignmentParameters.algorithm}' "
                f"'{self.params.BlankAssignmentParameters.value}' between samples and "
                f"sample blanks was compared."
            )
        else:
            self.summary.append(
                f"During blank assignment, an error occurred, and the "
                f"module terminated prematurely. For more information, see the logs."
            )

    def summarize_groupfactassignmentparameters(self: Self):
        if not (
            self.params.GroupFactAssignmentParameters
            and self.params.GroupFactAssignmentParameters.activate_module
        ):
            return

        if (
            self.params.GroupFactAssignmentParameters.activate_module
            and self.params.GroupFactAssignmentParameters.module_passed
        ):
            self.summary.append(
                f"Samples were grouped according to the provided group metadata "
                f"information. For each molecular feature observed in more than one "
                f"group, the quotient between the "
                f"'{self.params.GroupFactAssignmentParameters.algorithm}' "
                f"'{self.params.GroupFactAssignmentParameters.value}' "
                f"of groups was calculated pairwise."
            )
        else:
            self.summary.append(
                f"During group metadata assignment, an error occurred, and the "
                f"module terminated prematurely. For more information, see the logs."
            )

    def summarize_phenoqualassgnparams(self: Self):
        if not (
            self.params.PhenoQualAssgnParams
            and self.params.PhenoQualAssgnParams.activate_module
        ):
            return

        if (
            self.params.PhenoQualAssgnParams.activate_module
            and self.params.PhenoQualAssgnParams.module_passed
        ):
            self.summary.append(
                f"Molecular feature only detected in phenotype-associated samples "
                f"were considered phenotype-associated, as were feature that had a "
                f"quotient of higher than "
                f"'{self.params.PhenoQualAssgnParams.factor}' when their "
                f"'{self.params.PhenoQualAssgnParams.algorithm}' "
                f"'{self.params.PhenoQualAssgnParams.value}' between "
                f"phenotype-associated and not phenotype-associated "
                f"samples was compared."
            )
        else:
            self.summary.append(
                f"During assignment of phenotype data, an error occurred, and the "
                f"module terminated prematurely. For more information, see the logs."
            )

    def summarize_phenoquantpercentassgnparams(self: Self):
        if not (
            self.params.PhenoQuantPercentAssgnParams
            and self.params.PhenoQuantPercentAssgnParams.activate_module
        ):
            return

        if (
            self.params.PhenoQuantPercentAssgnParams.activate_module
            and self.params.PhenoQuantPercentAssgnParams.module_passed
        ):
            self.summary.append(
                f"For each molecular feature detected in more than three "
                f"phenotype-associated samples, the "
                f"'{self.params.PhenoQuantPercentAssgnParams.sample_avg}' "
                f"'{self.params.PhenoQuantPercentAssgnParams.value}' was correlated "
                f"with the percentage activity per sample using "
                f"'{self.params.PhenoQuantPercentAssgnParams.algorithm}' correlation "
                f"and the feature was only considered phenotype-associated if its "
                f"coefficient was greater than "
                f"'{self.params.PhenoQuantPercentAssgnParams.coeff_cutoff}' and its "
                f"{self.params.PhenoQuantPercentAssgnParams.fdr_corr}-corrected p-value less than "
                f"'{self.params.PhenoQuantPercentAssgnParams.p_val_cutoff}'"
                f"."
            )
        else:
            self.summary.append(
                f"During assignment of phenotype data, an error occurred, and the "
                f"module terminated prematurely. For more information, see the logs."
            )

    def summarize_phenoquantconcassgnparams(self: Self):
        if not (
            self.params.PhenoQuantConcAssgnParams
            and self.params.PhenoQuantConcAssgnParams.activate_module
        ):
            return

        if (
            self.params.PhenoQuantConcAssgnParams.activate_module
            and self.params.PhenoQuantConcAssgnParams.module_passed
        ):
            self.summary.append(
                f"For each molecular feature detected in more than three "
                f"phenotype-associated samples, the "
                f"'{self.params.PhenoQuantConcAssgnParams.sample_avg}' "
                f"'{self.params.PhenoQuantConcAssgnParams.value}' was correlated "
                f"with the inverse concentration per sample using "
                f"'{self.params.PhenoQuantConcAssgnParams.algorithm}' correlation "
                f"and the feature was only considered phenotype-associated if its "
                f"coefficient was greater than "
                f"'{self.params.PhenoQuantConcAssgnParams.coeff_cutoff}' and its "
                f"{self.params.PhenoQuantConcAssgnParams.fdr_corr}-corrected p-value less than "
                f"'{self.params.PhenoQuantConcAssgnParams.p_val_cutoff}'"
                f"."
            )
        else:
            self.summary.append(
                f"During assignment of phenotype data, an error occurred, and the "
                f"module terminated prematurely. For more information, see the logs."
            )

    def summarize_spectrallibmatchingcosineparameters(self: Self):
        if not (
            self.params.SpectralLibMatchingCosineParameters
            and self.params.SpectralLibMatchingCosineParameters.activate_module
        ):
            return

        if (
            self.params.SpectralLibMatchingCosineParameters.activate_module
            and self.params.SpectralLibMatchingCosineParameters.module_passed
        ):
            self.summary.append(
                f"The MS/MS spectrum of each molecular feature was matched pairwise "
                f"against the user-provided spectral library using the 'modified "
                f"cosine' algorithm, with a fragment tolerance of "
                f"'{self.params.SpectralLibMatchingCosineParameters.fragment_tol}'. "
                f"Matches were only retained if the number of matched peaks "
                f"between feature and library spectrum was greater than "
                f"'{self.params.SpectralLibMatchingCosineParameters.min_nr_matched_peaks}'"
                f", the score exceeded the cutoff score of "
                f"'{self.params.SpectralLibMatchingCosineParameters.score_cutoff}', "
                f"and the maximum precursor m/z difference of "
                f"'{self.params.SpectralLibMatchingCosineParameters.max_precursor_mass_diff}"
                f"' was not exceeded."
            )
        else:
            self.summary.append(
                f"During spectral library matching using the modified cosine "
                f"algorithm, an error occurred, and the "
                f"module terminated prematurely. For more information, see the logs."
            )

    def summarize_spectrallibmatchingdeepscoreparameters(self: Self):
        if not (
            self.params.SpectralLibMatchingDeepscoreParameters
            and self.params.SpectralLibMatchingDeepscoreParameters.activate_module
        ):
            return

        if (
            self.params.SpectralLibMatchingDeepscoreParameters.activate_module
            and self.params.SpectralLibMatchingDeepscoreParameters.module_passed
        ):
            self.summary.append(
                f"The MS/MS spectrum of each molecular feature was matched pairwise "
                f"against the user-provided spectral library using the 'MS2DeepScore"
                f"' algorithm. "
                f"Matches were only retained if the score exceeded the cutoff score of "
                f"'{self.params.SpectralLibMatchingDeepscoreParameters.score_cutoff}', "
                f"and the maximum precursor m/z difference of "
                f"'{self.params.SpectralLibMatchingDeepscoreParameters.max_precursor_mass_diff}"
                f"' was not exceeded."
            )
        else:
            self.summary.append(
                f"During spectral library matching using the MS2DeepScore "
                f"algorithm, an error occurred, and the "
                f"module terminated prematurely. For more information, see the logs."
            )

    def summarize_askcbcosinematchingparams(self: Self):
        if not (
            self.params.AsKcbCosineMatchingParams
            and self.params.AsKcbCosineMatchingParams.activate_module
        ):
            return

        if (
            self.params.AsKcbCosineMatchingParams.activate_module
            and self.params.AsKcbCosineMatchingParams.module_passed
        ):
            self.summary.append(
                f"The MS/MS spectrum of each molecular feature was matched pairwise "
                f"against a targeted spectral library constructed from relevant "
                f"matches of the KnownClusterBlast algorithm. Matching was performed "
                f"using the 'modified cosine' algorithm, with a fragment tolerance "
                f"of '{self.params.AsKcbCosineMatchingParams.fragment_tol}' and "
                f"matches were only retained "
                f"if the number of matched peaks "
                f"between feature and library spectrum was greater than "
                f"'{self.params.AsKcbCosineMatchingParams.min_nr_matched_peaks}'"
                f", the score exceeded the cutoff score of "
                f"'{self.params.AsKcbCosineMatchingParams.score_cutoff}', "
                f"and the maximum precursor m/z difference of "
                f"'{self.params.AsKcbCosineMatchingParams.max_precursor_mass_diff}"
                f"' was not exceeded."
            )
        else:
            self.summary.append(
                f"During annotation using the antiSMASH KnownClusterBlast results, "
                f"an error occurred in the modified cosine-based matching, and the "
                f"module terminated prematurely. For more information, see the logs."
            )

    def summarize_askcbdeepscorematchingparams(self: Self):
        if not (
            self.params.AsKcbDeepscoreMatchingParams
            and self.params.AsKcbDeepscoreMatchingParams.activate_module
        ):
            return

        if (
            self.params.AsKcbDeepscoreMatchingParams.activate_module
            and self.params.AsKcbDeepscoreMatchingParams.module_passed
        ):
            self.summary.append(
                f"The MS/MS spectrum of each molecular feature was matched pairwise "
                f"against a targeted spectral library constructed from relevant "
                f"matches of the KnownClusterBlast algorithm. Matching was performed "
                f"using the 'MS2DeepScore' algorithm, and "
                f"matches were only retained "
                f"if the score exceeded the cutoff score of "
                f"'{self.params.AsKcbDeepscoreMatchingParams.score_cutoff}', "
                f"and the maximum precursor m/z difference of "
                f"'{self.params.AsKcbDeepscoreMatchingParams.max_precursor_mass_diff}"
                f"' was not exceeded."
            )
        else:
            self.summary.append(
                f"During annotation using the antiSMASH KnownClusterBlast results, "
                f"an error occurred in the MS2DeepScore-based matching, and the "
                f"module terminated prematurely. For more information, see the logs."
            )

    def assemble_summary(self: Self):
        """Call methods to assemble the summary file"""
        try:
            logger.debug("'SummaryWriter': Started summary: files")
            self.summarize_peaktableparameters()
            self.summarize_msmsparameters()
            self.summarize_phenotypeparameters()
            self.summarize_groupmetadataparameters()
            self.summarize_speclibparameters()
            self.summarize_ms2queryresultsparameters()
            self.summarize_asresultsparameters()
            logger.debug("'SummaryWriter': Completed summary: files")
            logger.debug("'SummaryWriter': Started summary: analysis modules")
            self.summarize_featurefilteringparameters()
            self.summarize_adductannotationparameters()
            self.summarize_neutrallossparameters()
            self.summarize_fragmentannparameters()
            self.summarize_specsimnetworkcosineparameters()
            self.summarize_specsimnetworkdeepscoreparameters()
            self.summarize_blankassignmentparameters()
            self.summarize_groupfactassignmentparameters()
            self.summarize_phenoqualassgnparams()
            self.summarize_phenoquantpercentassgnparams()
            self.summarize_phenoquantconcassgnparams()
            self.summarize_spectrallibmatchingcosineparameters()
            self.summarize_spectrallibmatchingdeepscoreparameters()
            self.summarize_askcbcosinematchingparams()
            self.summarize_askcbdeepscorematchingparams()
            logger.debug("'SummaryWriter': Completed summary: analysis modules")
        except Exception as e:
            logger.error(str(e))
            logger.error(
                "SummaryWriter: error occurred during writing of summary. "
                "Write steps until error occurred."
            )
