from PIL import Image
import os

charts_folder = 'charts'

for filename in os.listdir(charts_folder):
    if filename.endswith('.png'):
        filepath = os.path.join(charts_folder, filename)
        img = Image.open(filepath)
        img = img.convert('RGB').convert('RGBA')
        img.save(filepath, 'PNG', optimize=False)
        print(f"Fixed: {filename}")

print("✅ All charts fixed.")