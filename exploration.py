from PIL import Image

def chunk_image(image_path, chunk_size):
    # Open the image
    img = Image.open(image_path)
    #img = img.resize((400, 600), Image.Resampling.LANCZOS)
    img_width, img_height = img.size
    print(img.size)
    # Calculate the number of chunks in each dimension
    chunks_x = img_width // chunk_size + 1
    chunks_y = img_height // chunk_size + 1

    # Create a list to hold the chunked images
    chunked_images = []
    chunked_dims = []
    # Loop through the image and create chunks
    for y in range(0, chunks_y):
        for x in range(0, chunks_x):
            left = x * chunk_size
            upper = y * chunk_size
            right = left + chunk_size
            lower = upper + chunk_size

            # Crop the image to create a chunk
            chunk = img.crop((left, upper, right, lower))
            chunked_images.append(chunk)
            chunked_dims.append((left, upper, right, lower))
    return chunked_images, chunked_dims
# Example usage
image_path = 'letter_of_recommendation_3.jpg'  # Replace with your image path
chunk_size = 100  # Define the size of each chunk

# Get the list of chunked images
chunks, dims = chunk_image(image_path, chunk_size)

# Save each chunk as a separate image file
for i, chunk in enumerate(chunks):
    chunk.save(f'chunk_{i}.png')

print(f"Image has been broken into {len(chunks)} chunks and saved as separate files.")

# each chunked image file should then get passed to Azure OpenAI gpt-4o model to see if there are any evidence of alteration.


# generating the heatmap
from PIL import Image, ImageDraw

def overlay_boxes(image_path):
    # Open the image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img, "RGBA")

    # Define the colors with 50% transparency
    green_color = (0, 255, 0, 127)  # RGBA
    red_color = (255, 0, 0, 128)
    ind = 0
    # Draw the boxes
    for dim in dims:
        if ind == 2 or ind == 3:
            draw.rectangle(dim, fill=red_color)
            draw.rectangle(dim, outline=(0, 0, 0, 127), width=3)
        else:
            draw.rectangle(dim, fill=green_color)
            draw.rectangle(dim, outline=(0, 0, 0, 127), width=3)
        ind = ind + 1
    # Save the image with overlay
    img.save("overlay_image.png")

# Example usage
image_path = 'letter_of_recommendation_3.jpg'  # Replace with your image path
overlay_boxes(image_path)
