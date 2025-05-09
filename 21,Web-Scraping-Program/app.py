import requests
from bs4 import BeautifulSoup

def scrape_github_profile_image(username):
    url = f"https://github.com/{username}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # Extract the image tag
            image_tag = soup.find("img", {"alt": "Avatar"})
            if image_tag and 'src' in image_tag.attrs:
                image_url = image_tag['src']
                print(f"✅ Profile image found: {image_url}")
                return image_url
            else:
                print("❌ Could not find profile image.")
        else:
            print(f"❌ Failed to fetch profile. Status code: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Error: {e}")

    return None

# Optional: Function to download the image
def download_image(image_url, username):
    try:
        img_data = requests.get(image_url).content
        filename = f"{username}_avatar.jpg"
        with open(filename, "wb") as f:
            f.write(img_data)
        print(f"✅ Image downloaded successfully as {filename}")
    except Exception as e:
        print(f"⚠️ Error downloading image: {e}")

# 🧪 Run the program
if __name__ == "__main__":
    print("🔍 GitHub Profile Image Scraper")
    user = input("Enter a GitHub username: ").strip()
    img_url = scrape_github_profile_image(user)

    if img_url:
        download = input("Do you want to download the image? (yes/no): ").lower()
        if download == "yes":
            download_image(img_url, user)

