from PIL import Image

#enter your src
BILLET_SRC = "C:\\Users\\User\\Desktop\\work\\photo\\benefit.png"
IMAGE_SRC = "C:\\Users\\User\\Desktop\\work\\photo\\image.jpg"
RESULT_SRC = "C:\\Users\\User\\Desktop\\work\\photo\\result.jpg"

def process_images(image , billet , result ):
    try:
        #open images
        image_i = Image.open(image)
        billet_i = Image.open(billet)

        #create new image
        result_i = Image.new('RGB', (image_i.width if image_i.width > billet_i.width else billet_i.width, image_i.height+billet_i.height // 3))

        #past image in new
        result_i.paste(billet_i, (0,0))
        result_i.paste(image_i, (0,150))

        #save
        result_i.save(result, quality=100)
        print("The image is saved correctly. Bye!")
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    process_images(IMAGE_SRC, BILLET_SRC, RESULT_SRC)
