#
# An annotator service to identify biomedical concepts in plain text.
# Source code: https://github.com/RENCI-NER/nemo-serve
# Hosted at: https://med-nemo.apps.renci.org/docs
#

import requests

from renci_ner.core import AnnotatedText, Annotation, AnnotationProvenance, Annotator

# Configuration.
RENCI_BIOMEGATRON_URL = "https://med-nemo.apps.renci.org"


class BioMegatron(Annotator):
    """
    Provides an Annotator interface to a BioMegatron service.
    """

    @property
    def provenance(self) -> AnnotationProvenance:
        """Return an AnnotationProvenance describing annotations produced by this service."""
        return AnnotationProvenance(
            name="BioMegatron", url=RENCI_BIOMEGATRON_URL, version=self.openapi_version
        )

    def __init__(
        self,
        url=RENCI_BIOMEGATRON_URL,
        requests_session=requests.Session(),
        timeout=120,
    ):
        """
        Set up a BioMegatron service.

        :param url: The URL of the BioMegatron service.
        :param requests_session: A Requests session object to use instead of the default one.
        :param timeout: The timeout to use for requests in seconds. Default: 120 seconds.
        """
        self.url = url
        self.annotate_url = url + "/annotate/"
        self.requests_session = requests_session

        result = self.requests_session.get(self.url + "/openapi.json", timeout=timeout)
        result.raise_for_status()
        openapi_data = result.json()
        self.openapi_version = openapi_data.get("info", {"version": "NA"}).get(
            "version", "NA"
        )

    def supported_properties(self):
        """Some configurable parameters for BioMegatron (none at present)."""
        return {
            "timeout": "The timeout in seconds for requests to BioMegatron. Default: 120 seconds."
        }

    def annotate(self, text: str, props: dict = None) -> AnnotatedText:
        """
        Annotate text using BioMegatron.

        :param text: Text to annotate.
        :param props: Properties to pass to BioMegatron.
        :return: An AnnotatedText object containing the annotations.
        """

        if props is None:
            props = {}

        session = self.requests_session
        timeout = props.get("timeout", 120)

        response = session.post(
            self.annotate_url,
            json={
                "text": text,
                "model_name": "token_classification",
            },
            timeout=timeout,
        )

        response.raise_for_status()

        result = response.json()

        annotations = []
        for denotation in result.get("denotations", []):
            span = denotation.get("span", {})
            start_index = span.get("begin", -1)
            end_index = span.get("end", -1)

            annotations.append(
                Annotation(
                    text=denotation.get("text", ""),
                    start=start_index,
                    end=end_index,
                    id=denotation.get("id", ""),
                    label="",
                    type=denotation.get("obj", ""),
                    props={},
                    provenance=self.provenance,
                )
            )

        return AnnotatedText(text, annotations)
