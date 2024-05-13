import pdf2image


def convert_to_image(pdf: str, pdf_name: str):
    pages = pdf2image.convert_from_path( f'{pdf}',500,  poppler_path = r'C:/Users/khurr/Downloads/poppler-22.04.0/Library/bin')

    for i in range(len(pages)):

        pages[i].save('./bizdevs-attachments/'+f'{pdf_name}_img'+ str(i) +'.jpg', 'JPEG')
        img_path = './bizdevs-attachments/'+f'{pdf_name}_img'+ str(i) +'.jpg'
    return img_path