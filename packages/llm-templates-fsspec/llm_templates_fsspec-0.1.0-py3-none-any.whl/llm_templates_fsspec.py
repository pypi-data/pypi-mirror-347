from llm import Template, hookimpl


@hookimpl
def register_template_loaders(register):
    register("local", fsspec_template_loader)


def fsspec_template_loader(template_path: str) -> Template:
    ...