import requests
from .exceptions import DhwaniAPIError

def document_ocr(client, file_path, language=None):
    """OCR a document (image/PDF) and return extracted text."""
    with open(file_path, "rb") as f:
        files = {"file": f}
        data = {}
        if language:
            data["language"] = language
        resp = requests.post(
            f"{client.api_base}/v1/document/ocr",
            headers=client._headers(),
            files=files,
            data=data
        )
    if resp.status_code != 200:
        raise DhwaniAPIError(resp)
    return resp.json()

def document_summarize(client, file_path, page_number=1, src_lang="eng_Latn", tgt_lang="kan_Knda"):
    """Summarize a PDF document with language and page number options."""
    url = f"{client.api_base}/v1/indic-summarize-pdf"
    headers = client._headers()
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "application/pdf")}
        data = {
            "page_number": str(page_number),
            "src_lang": src_lang,
            "tgt_lang": tgt_lang
        }
        resp = requests.post(
            url,
            headers=headers,
            files=files,
            data=data
        )
    if resp.status_code != 200:
        raise DhwaniAPIError(resp)
    return resp.json()


def extract(client, file_path, page_number, src_lang, tgt_lang):
    """
    Extract and translate text from a document (image/PDF) using query parameters.
    """
    # Build the URL with query parameters
    url = (
        f"{client.api_base}/v1/indic-extract-text/"
        f"?page_number={page_number}&src_lang={src_lang}&tgt_lang={tgt_lang}"
    )
    headers = client._headers()
    # 'requests' handles multipart/form-data automatically
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "application/pdf")}
        resp = requests.post(
            url,
            headers=headers,
            files=files
        )
    if resp.status_code != 200:
        raise DhwaniAPIError(resp)
    return resp.json()

def doc_query(
    client,
    file_path,
    page_number=1,
    prompt="list the key points",
    src_lang="eng_Latn",
    tgt_lang="kan_Knda"
):
    """Query a document with a custom prompt and language options."""
    url = f"{client.api_base}/v1/indic-custom-prompt-pdf"
    headers = client._headers()
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "application/pdf")}
        data = {
            "page_number": str(page_number),
            "prompt": prompt,
            "source_language": src_lang,
            "target_language": tgt_lang
        }
        resp = requests.post(
            url,
            headers=headers,
            files=files,
            data=data
        )
    if resp.status_code != 200:
        raise DhwaniAPIError(resp)
    return resp.json()


def doc_query_kannada(
    client, 
    file_path, 
    page_number=1, 
    prompt="list key points", 
    src_lang="eng_Latn",
    language=None
):
    """Summarize a document (image/PDF/text) with custom prompt and language."""
    url = f"{client.api_base}/v1/indic-custom-prompt-kannada-pdf"
    headers = client._headers()
    # 'requests' will handle multipart/form-data automatically
    with open(file_path, "rb") as f:
        files = {"file": (file_path, f, "application/pdf")}
        data = {
            "page_number": str(page_number),
            "prompt": prompt,
            "src_lang": src_lang,
        }
        if language:
            data["language"] = language
        resp = requests.post(
            url,
            headers=headers,
            files=files,
            data=data
        )
    if resp.status_code != 200:
        raise DhwaniAPIError(resp)
    return resp.json()



class Documents:
    @staticmethod
    def ocr(file_path, language=None):
        from . import _get_client
        return _get_client().document_ocr(file_path, language)

    @staticmethod
    def summarize(*args, **kwargs):
        from . import _get_client
        return _get_client().document_summarize(*args, **kwargs)
    @staticmethod
    def run_extract(*args, **kwargs):
        from . import _get_client
        return _get_client().extract(*args, **kwargs)
    @staticmethod
    def run_doc_query(*args, **kwargs):
        from . import _get_client
        return _get_client().doc_query(*args, **kwargs)
    @staticmethod
    def run_doc_query_kannada(*args, **kwargs):
        from . import _get_client
        return _get_client().doc_query_kannada(*args, **kwargs)