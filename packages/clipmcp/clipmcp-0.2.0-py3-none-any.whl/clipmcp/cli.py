import click
from .services.image_service import generate_image

@click.command()
@click.argument('prompt')
@click.option('--output', default='./output_images', help='Output directory')
def main(prompt, output):
    """Generate images from text prompts using CLIP model"""
    click.echo(f"Generating image for prompt: '{prompt}'")
    result = generate_image(prompt, output_dir=output)
    click.echo(f"Image saved to: {result['path']}")

if __name__ == "__main__":
    main()