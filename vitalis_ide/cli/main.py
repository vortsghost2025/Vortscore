import click
from vitalis_ide.brain.thinker import ThinkingProcess
from vitalis_ide.brain.ghost_explain import GhostExplain
from vitalis_ide.brain.rag import LocalRAG

@click.group()
def cli():
    pass

@cli.command()
@click.argument('input_text')
def think(input_text):
    thinker = ThinkingProcess()
    thinker.run(input_text)

@cli.command()
def explain():
    explainer = GhostExplain()
    click.echo(explainer.get_narrative())

@cli.command()
@click.argument('query')
def query_rag(query):
    rag = LocalRAG()
    click.echo(rag.retrieve(query))

if __name__ == '__main__':
    cli()
