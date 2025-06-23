from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import PdfReader, PdfWriter


def impr(employe,sal):




 def xgimp_to_reportlab(x_gimp, dpi=150, image_height_px=1755):
    x = x_gimp * 72 / dpi
    
    return x



 def ygimp_to_reportlab( y_gimp, dpi=150, image_height_px=1755):
   
    y = (image_height_px - y_gimp) * 72 / dpi
    return y


 # 4 pixel de differnce en y

 def create_overlay_pdf(data_dict, overlay_path="overlay.pdf"):
    c = canvas.Canvas(overlay_path, pagesize=A4)
    c.setFont("Helvetica-Bold", 12)
    # Example positions (you must measure from your actual PDF!)
    c.drawString(xgimp_to_reportlab(268), ygimp_to_reportlab(262),employe[1] )
    c.drawString(xgimp_to_reportlab(934),ygimp_to_reportlab(1592) , str(round(sal,2)))
    

    c.save()



 def fill_pdf_form(template_path, overlay_path, output_path="filled.pdf"):
    template = PdfReader(template_path)
    overlay = PdfReader(overlay_path)
    writer = PdfWriter()

    base_page = template.pages[0]
    overlay_page = overlay.pages[0]
    base_page.merge_page(overlay_page)  # Merge text over template

    writer.add_page(base_page)

    with open(output_path, "wb") as f:
        writer.write(f)


 data_dict = {
    "employe": employe[1],
    "sala": str(sal),
   
}
 create_overlay_pdf(data_dict)
 fill_pdf_form("fiche.pdf", "overlay.pdf", "salaire_final.pdf")       