import json

class JsonSerializableMixin:
    """Mixin para adicionar capacidade de serializacao basica."""
    def to_json_str(self) -> str:
        if hasattr(self, 'to_dict'):
            return json.dumps(self.to_dict(), ensure_ascii=False)
        return "{}"

class ExibivelMixin:
    """Mixin para padronizar exibicao textual."""
    def obter_resumo(self) -> str:
        return str(self)