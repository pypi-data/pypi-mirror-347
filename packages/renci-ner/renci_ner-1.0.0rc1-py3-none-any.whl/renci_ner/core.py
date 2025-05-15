from dataclasses import dataclass, field
from typing import Self


@dataclass
class AnnotationProvenance:
    """
    The provenance of an annotation. The goal is to simply record the name, URL, and version of the service that
    produced this annotation -- in the future, we might also want to record the properties used in making this
    annotation.
    """

    name: str
    url: str
    version: str


@dataclass
class Annotation:
    """
    A class for storing a single annotation.

    The `based_on` field is a list of other annotations that this annotation is based on, in order of annotation:
    for example, if you run an annotation through BioMegatron, then SAPBERT, then NodeNorm, the BioMegatron annotation
    will be at `based_on[0]`, SAPBERT annotation will be at `based_on[1]`, and NodeNorm annotation will be at
    `based_on[2]`.
    """

    text: str
    id: str
    label: str
    type: str
    start: int
    end: int
    provenance: AnnotationProvenance
    based_on: list[Self] = field(default_factory=list)
    props: dict = field(default_factory=dict)

    @property
    def provenances(self) -> list[AnnotationProvenance]:
        """Return a list of provenances for this annotation and its based_on annotations."""
        return list(map(lambda ann: ann.provenance, self.based_on)) + [self.provenance]


@dataclass
class NormalizedAnnotation(Annotation):
    """
    A NormalizedAnnotation is an Annotation that has been normalized. It has a Biolink type (starting with `biolink:`),
    and the ID is expected to be a CURIE.
    """

    biolink_type: str = None

    def __setattr__(self, name, value):
        """Validate biolink_type."""
        if (
            name == "biolink_type"
            and value is not None
            and not value.lower().startswith("biolink:")
        ):
            raise ValueError(
                f"Invalid biolink_type: must start with 'biolink:' but got '{value}'."
            )

        # TODO: it'd probably be a good idea to check formatting for CURIEs as well, but that's less well defined.

        # No problems.
        super().__setattr__(name, value)

    @classmethod
    def from_annotation(
        cls,
        annotation: Annotation,
        provenance: AnnotationProvenance,
        curie=None,
        biolink_type=None,
        label=None,
    ) -> Self:
        """
        Creates an instance of NormalizedAnnotation from the provided Annotation object.
        This mostly consists of copying the fields from the original Annotation, but
        the label, ID and Biolink type is expected to be overridden.

        :param annotation: The Annotation instance used as the basis for constructing
            the NormalizedAnnotation object.
        :type annotation: Annotation
        :param provenance: The provenance of the normalized annotation.
        :type provenance: AnnotationProvenance
        :param curie: Optional CURIE string for additional annotation details. If not
            provided, it defaults to None.
        :type curie: str, optional
        :param biolink_type: Optional biolink type string to specify the type of the
            annotation. If not provided, it defaults to None.
        :type biolink_type: str, optional
        :param label: Optional label string to specify the label of the annotation. Will overwrite the
            annotation label if one is provided.
        :type label: str, optional
        :return: A new instance of NormalizedAnnotation initialized with the provided
            annotation and optional parameters.
        :rtype: Self
        """

        if label is None:
            label = annotation.label

        if curie is None:
            curie = annotation.id

        if biolink_type is None:
            biolink_type = annotation.type

        return NormalizedAnnotation(
            text=annotation.text,
            start=annotation.start,
            end=annotation.end,
            provenance=provenance,
            based_on=[*annotation.based_on, annotation],
            props=annotation.props,
            # These fields are overwritten during normalization.
            id=curie,
            label=label,
            type=biolink_type,
            biolink_type=biolink_type,
        )


@dataclass
class AnnotatedText:
    """
    A class for storing a text along with a set of annotations from a single source.
    """

    text: str
    annotations: list[Annotation] = field(default_factory=list)

    def transform(self, transformer: "Transformer", props: dict = None) -> Self:
        """
        Transform the annotations in this AnnotatedText with a transformer.

        Note that in this case the Transformer is responsible for updating the provenance of the transformed annotations.

        :param transformer: A Transformer to transform this annotated text.
        :param props: The properties to pass to the transformer.
        :return: The transformed AnnotatedText.
        """
        if props is None:
            props = {}

        return transformer.transform(self, props)

    def reannotate(self, annotator: "Annotator", props: dict = None) -> Self:
        """
        Reannotate the annotations in this AnnotatedText with another annotator.

        Note that this does NOT mean that the original text is reannotated -- rather, each individual annotation
        will be annotated by the next annotator. This allows us to standardize some common situations:
        - If an annotation could not be annotated by the next annotator, it will be left as-is.
        - If an annotation is annotated by the next annotator with a single annotation, we will replace the previous
          annotation with this annotation, but update provenance and based_on fields.
        - If an annotation is annotated by the next annotator with multiple annotations, we will replace this
          annotation with all of those annotations, with provenance and based_on fields updated appropriately.

        :param annotator: The other annotator to annotate these annotations with.
        :type annotator: Annotator
        :param props: A dictionary of properties to pass to the annotator.
        :return: AnnotatedText with annotations re-annotated with the other annotator.
        """

        if props is None:
            props = {}

        new_annotations = []
        for annotation in self.annotations:
            annotated_text = annotator.annotate(annotation.text, props=props)
            reannotations = annotated_text.annotations
            if len(reannotations) == 0:
                # Leave the current annotation unchanged.
                new_annotations.append(annotation)
            else:
                # We have one or more annotations. So we need to update the based_on by adding annotation to the
                # existing list.
                new_based_on = [*annotation.based_on, annotation]
                base_start = annotation.start

                for reannotation in reannotations:
                    # Fix the start and end indices.
                    new_start = reannotation.start

                    text_size = len(reannotation.text)
                    assert text_size == (reannotation.end - reannotation.start)

                    reannotation.start = base_start + new_start
                    reannotation.end = base_start + new_start + text_size

                    reannotation.provenance = annotator.provenance
                    reannotation.based_on = new_based_on

                    new_annotations.append(reannotation)

        return AnnotatedText(self.text, new_annotations)


class Annotator:
    """
    An interface for a service that can annotate text.
    """

    @property
    def provenance(self) -> AnnotationProvenance:
        """
        Return an AnnotationProvenance describing annotations produced by this service.

        :return AnnotationProvenance: The provenance of annotations generated by this Annotator.:
        """
        return AnnotationProvenance(
            name="Annotator",
            url="http://example.org/",
            version="0.0.1",
        )

    def annotate(self, text: str, props: dict = None) -> AnnotatedText:
        """
        Annotate a text. Service-specific properties (see supported_properties for descriptions) can be passed in via
        `props`.

        :param text: The text to annotate.
        :param props: Properties supported by this annotator to use during the annotation.
        :return AnnotatedText: The annotated text.
        """
        return AnnotatedText(text, [])

    def supported_properties(self) -> dict[str, str]:
        """
        Return a dictionary of supported properties for this service. The keys are the property names, and the values
        are descriptions of the properties.

        :return: A dictionary of supported properties, with the values describing each property.
        """
        return {}


class Transformer:
    """
    An interface for transforming annotated text.
    """

    def supported_properties(self) -> dict[str, str]:
        """
        Return a dictionary of supported properties for this service. The keys are the property names, and the values
        are descriptions of the properties.

        :return: A dictionary of supported properties, with the values describing each property.
        """
        return {}

    def transform(
        self, annotated_text: AnnotatedText, props: dict = None
    ) -> AnnotatedText:
        """
        Transform an annotated text into a new annotated text.

        Note that in this case the Transformer is responsible for updating the provenance of the transformed annotations.

        :param annotated_text: The annotated text to transform.
        :param props: Properties supported by this transformer to use during the transformation.
        :return: The transformed AnnotatedText.
        """
        return annotated_text
