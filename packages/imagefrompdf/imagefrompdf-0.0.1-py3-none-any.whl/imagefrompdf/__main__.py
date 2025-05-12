import sys
import getpass
import traceback
from pathlib import Path
from pdf2image import convert_from_path
import click

def get_downloads_dir() -> Path:
    """Intenta encontrar la carpeta de Descargas del usuario."""
    home = Path.home()
    downloads = home / "Descargas"
    if downloads.exists():
        return downloads
    else:
        # Fallback genérico si no se encuentra Downloads
        return home

@click.command()
@click.argument("pdf_path", type=click.Path(exists=True))
@click.option("--format", default="png", type=click.Choice(["png", "jpg"]), help="Formato de salida: png o jpg")
def main(pdf_path, format):
    """Convierte un PDF en imágenes y las guarda en la carpeta de Descargas del usuario."""
    try:
        pdf_path = Path(str(pdf_path))

        # Validar si es realmente un archivo PDF
        if pdf_path.suffix.lower() != ".pdf":
            click.echo("❌ El archivo no es un PDF válido.")
            sys.exit(1)

        # Obtener el usuario y carpeta de descargas
        user = getpass.getuser()
        downloads_dir = get_downloads_dir()

        # Carpeta de salida con el mismo nombre que el PDF
        output_dir = downloads_dir / pdf_path.stem
        output_dir.mkdir(exist_ok=True)

        click.echo(f"👤 Usuario: {user}")
        click.echo(f"📥 Guardando imágenes en: {output_dir}")

        # Convertir el PDF a imágenes
        images = convert_from_path(str(pdf_path))
        for i, img in enumerate(images, start=1):
            img_name = f"page_{i}.{format}"
            img_path = output_dir / img_name
            img.save(img_path, format.upper())
            click.echo(f"✅ Página {i} guardada como {img_name}")

        click.secho(f"\n🎉 ¡Proceso completado! Las imágenes están en: {output_dir}", fg="green")

    except Exception as e:
        click.secho("❌ Error durante la conversión:", fg="red")
        click.secho(str(e), fg="red")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
