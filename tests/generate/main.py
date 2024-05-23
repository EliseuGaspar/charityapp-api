from fpdf import FPDF

CHANEL = 'Multicaixa Express'
Txt = """
    Banco de Origem > BAI \n
    Banco de Destino > BCI \n
    Motante > 20.000,00
"""

class PDF:
    @classmethod
    def generate(cls, extracts_account: str, ref_account: int, name_account: str):
        """generate extract pdf"""
        instance_fpdf = FPDF()
        instance_fpdf.add_page()
        instance_fpdf.set_font("Arial", size=12)
        instance_fpdf.image("Logo.png", x=90, y=14, w=35)
        instance_fpdf.cell(194,72,f"Operação realizada pelo canal {CHANEL}",0,0,'C')
        instance_fpdf.set_font('Times', '', 9)
        instance_fpdf.write(40, f"{Txt}")
        instance_fpdf.output("extract-1.pdf")
    
    @classmethod
    def set_line_text(cls, text: str, num_breaks: int = 1):
        """set breaks in text"""
        text_to_insert = ""
        for c in range(num_breaks):
            text_to_insert += "\n"
        return text_to_insert+text

PDF().generate('736598345892', '0F8768JJLK6756', 'Eliseu Gaspar')