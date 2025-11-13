from odoo import models, fields
import os


class XMLGenerate(models.TransientModel):
    _name = "xml.generate"
    _description = "XML Generate"

    module_path = fields.Char(string="Module", required=True)
    model_ids = fields.Many2many("ir.model", string="Model", required=True)

    def generate(self):
        self.ensure_one()

        views_dir = os.path.join(self.module_path, "views")
        os.makedirs(views_dir, exist_ok=True)

        for model in self.model_ids:
            model_name = model.model
            model_file_safe = model_name.replace(".", "_")
            file_name = f"{model_file_safe}.xml"
            file_path = os.path.join(views_dir, file_name)
            print(model_name, file_path, file_name)

            required_fields = model.field_id.filtered(lambda x: x.required)

            if not required_fields:
                continue

            with open(file_path, "w", encoding="utf-8") as f:
                f.write('<?xml version="1.0" encoding="utf-8"?>\n')
                f.write("<odoo>\n")
                f.write("    <data>\n\n")

                f.write(f'        <record id="{model_file_safe}_list" model="ir.ui.view">\n')
                f.write(f'            <field name="name">{model_name}.list</field>\n')
                f.write(f'            <field name="model">{model_name}</field>\n')
                f.write('            <field name="arch" type="xml">\n')
                f.write('                <list string="List">\n')
                for field in required_fields:
                    f.write(f'                    <field name="{field.name}"/>\n')
                f.write("                </list>\n")
                f.write("            </field>\n")
                f.write("        </record>\n\n")

                f.write(f'        <record id="{model_file_safe}_form" model="ir.ui.view">\n')
                f.write(f'            <field name="name">{model_name}.form</field>\n')
                f.write(f'            <field name="model">{model_name}</field>\n')
                f.write('            <field name="arch" type="xml">\n')
                f.write('                <form string="Form">\n')
                f.write('                    <sheet>\n')
                for field in required_fields:
                    f.write(f'                        <field name="{field.name}"/>\n')
                f.write("                    </sheet>\n")
                f.write("                </form>\n")
                f.write("            </field>\n")
                f.write("        </record>\n\n")

                f.write(f'        <record id="action_{model_file_safe}" model="ir.actions.act_window">\n')
                f.write(f'            <field name="name">{model_name.replace(".", " ").title()}</field>\n')
                f.write(f'            <field name="res_model">{model_name}</field>\n')
                f.write('            <field name="view_mode">tree,form</field>\n')
                f.write("        </record>\n\n")

                f.write(
                    f'        <menuitem id="menu_{model_file_safe}" name="{model_file_safe.replace("_", " ").title()}" action="action_{model_file_safe}"/>\n')

                f.write("    </data>\n")
                f.write("</odoo>\n")



