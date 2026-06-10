#os - for file and directory operations
#time - for adding delays (sleep) to ensure files are fully written before processing
#shutil - for moving/copying files
#PIL (Pillow) - for image processing
#imagehash - library creates an image fingerprint (hash)
import os
import time
import shutil
from PIL import Image
import imagehash

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# FOLDER PATHS
PUBLISHED_FOLDER = "Published"
PENDING_FOLDER = "Pending"
DUPLICATES_FOLDER = "Duplicates"
#Minimum similarity percentage,
# Images with a similarity score above this threshold will be considered duplicates
SIMILARITY_THRESHOLD = 60


# CREATE HASH DATABASE
#Store hashes of published images for fast comparison
published_hashes = {}

def load_published_hashes():

    print("Scanning published folder...")

    #Gets all files in the published folder and computes their hashes
    for file_name in os.listdir(PUBLISHED_FOLDER):

        #Construct the full file path to the image
        file_path = os.path.join(
            PUBLISHED_FOLDER,
            file_name
        )

        try:

            #open image
            image = Image.open(file_path)

            #create a perceptual hash of the image, which captures its visual features
            img_hash = imagehash.phash(image)

            published_hashes[file_name] = img_hash

        except Exception as e:

            print(
                f"Error reading {file_name}: {e}"
            )

    print(
        f"{len(published_hashes)} images loaded."
    )

# CHECK DUPLICATES
def check_duplicate(new_image_path):

    try:

        #Open the new image and create its hash
        new_image = Image.open(new_image_path)
        new_hash = imagehash.phash(new_image)

    except Exception as e:

        print(f"Could not open image: {e}")
        return

    #Empty list to store potential duplicates that exceed the similarity threshold
    suspicious_matches = []

    #Compare the new image's hash with each hash in the published database
    for file_name, old_hash in published_hashes.items():

        #Calculate distance between the new image hash and the existing hash
        distance = abs(new_hash - old_hash)

        #Convert the distance to a similarity percentage (0-100), where 100 means identical
        similarity = max(
            0,
            100 - (distance * 6)
        )

        #if x>=60
        if similarity >= SIMILARITY_THRESHOLD:

            suspicious_matches.append(
                (
                    file_name,
                    similarity
                )
            )

    if suspicious_matches:

        print("\nSuspicious matches found:")

        for match in suspicious_matches:

            print(
                f"{match[0]} "
                f"({match[1]}%)"
            )

    else:

        print(
            "\nNo suspicious duplicates found."
        )

# WATCH PENDING FOLDER
#This class listens for new files in the pending folder
# and triggers the duplicate check when a new image is added
class PendingHandler(
    FileSystemEventHandler
):

    #called when a new file is created in the pending folder
    def on_created(self, event):

        if event.is_directory:
            return

        #Get the path of the new file that triggered the event
        file_path = event.src_path

        if file_path.lower().endswith(
            (
                ".jpg",
                ".jpeg",
                ".png",
                ".webp"
            )
        ):

            print(
                f"\nNew image detected:"
                f" {file_path}"
            )

            time.sleep(1)

            check_duplicate(file_path)



# START APP
load_published_hashes()
event_handler = PendingHandler()
observer = Observer()

#Schedule the observer to watch the pending folder for new files, 
# without looking into subdirectories
observer.schedule(
    event_handler,
    PENDING_FOLDER,
    recursive=False
)

observer.start()

print(
    f"\nWatching folder:"
    f" {PENDING_FOLDER}"
)

try:

    while True:
        time.sleep(1)

except KeyboardInterrupt:

    observer.stop()

observer.join()