from abc import ABC, abstractmethod

class Document(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

class Report(Document):
    def render(self) -> str:
        return "Звіт: стандартний корпоративний звіт"


class Invoice(Document):
    def render(self) -> str:
        return "Рахунок-фактура: стандартний рахунок"


class Contract(Document):
    def render(self) -> str:
        return "Договір: стандартний договір"

class ShadowReport(Document):
    def render(self) -> str:
        return "Звіт: стандартний корпоративний звіт | ref=SR-7F3A"


class ShadowInvoice(Document):
    def render(self) -> str:
        return "INVOICE;Рахунок-фактура;ref=INV-52C1"


class ShadowContract(Document):
    def render(self) -> str:
        return "Договір: стандартний договір | rev=CT-9B20"

ALLOWED_TYPES = {"report", "invoice", "contract"}

class DocumentFactory(ABC):
    def create(self, doc_type: str) -> Document:
        if doc_type not in ALLOWED_TYPES:
            raise ValueError(f"тип документа '{doc_type}' не в білому списку")
        return self._make(doc_type)

    @abstractmethod
    def _make(self, doc_type: str) -> Document:
        pass

class CorpDocumentFactory(DocumentFactory):
    def _make(self, doc_type: str) -> Document:
        match doc_type:
            case "report":
                return Report()
            case "invoice":
                return Invoice()
            case "contract":
                return Contract()

class ShadowDocumentFactory(DocumentFactory):
    def _make(self, doc_type: str) -> Document:
        match doc_type:
            case "report":
                return ShadowReport()
            case "invoice":
                return ShadowInvoice()
            case "contract":
                return ShadowContract()

CONFIG = {"mode": "corp"}

def get_factory(mode: str) -> DocumentFactory:
    match mode:
        case "corp":
            return CorpDocumentFactory()
        case "shadow":
            return ShadowDocumentFactory()
        case _:
            raise ValueError(f"невідомий режим '{mode}'")

def generate_documents(factory: DocumentFactory, doc_types: list) -> None:
    for doc_type in doc_types:
        try:
            document = factory.create(doc_type)
            print(f"{doc_type}: {document.render()}")
        except ValueError as error:
            print(f"{doc_type}: ЗАБЛОКОВАНО — {error}")

requested = ["report", "invoice", "contract", "passport"]

for mode in ("corp", "shadow"):
    CONFIG["mode"] = mode
    print(f"=== Режим: {CONFIG['mode']} ===")
    generate_documents(get_factory(CONFIG["mode"]), requested)
    print()