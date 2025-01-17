# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies (<https://www.cybrosys.com>).
#    Author: Noushid Khan.P (<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################

import json

from odoo import models, fields, _
import http.client

from odoo.exceptions import UserError


class EmailTemplateDetails(models.Model):
    _name = "email.template"
    _rec_name = "temp_name"
    _description = "Template Creation"

    temp_name = fields.Char(string="Template Name", required=True)
    generation = fields.Char(string="Template Generation", default="Dynamic", readonly=True)
    ver_name = fields.Char(string="Version Name")
    ver_subject = fields.Char(string="Version Subject", required=True)
    ver_editor = fields.Selection([('design', "Design"), ('code', "Code")], string="Version Editor", default="design")
    temp_cont = fields.Html(string="Template Content", help="content convert to html code", translate=True,
                            sanitize=False)
    temp_id = fields.Char(string="Template ID")

    def create_temp(self):
        """
        function is used for creating Mail Template

        """
        api_key = ""
        company_id = self.env.company
        temp_name = self.temp_name
        temp_gen = self.generation
        api_info = self.env['ir.config_parameter'].search(
            [('key', '=', "SendGrid API Key " + company_id.name + "")])
        if not api_info:
            raise UserError(_("It Needs API Key"))
        if api_info.company_id.id == self.env.company.id:
            api_key = api_info.value
        if not api_key and api_key == "":
            raise UserError(_("Your Company Needs an API Key"))
        conn = http.client.HTTPSConnection("api.sendgrid.com")

        payload = "{\"name\":\"" + temp_name + "\",\"generation\":\"dynamic\"}"

        headers = {
            'authorization': "Bearer " + api_key + "",
            'content-type': "application/json"
        }

        conn.request("POST", "/v3/templates", payload, headers)

        res = conn.getresponse()
        print("res", res)
        data = res.read()
        print("data2", data)
        print("json", json)
        temp_data = json.loads(data.decode("utf-8"))
        print("temp_data", temp_data)
        self.temp_id = temp_data['id']

    def create_ver(self):
        """
        Function is used for creating mail content to the
        Created Template.

        """
        api_key = ""
        if self.temp_cont:
            print(self.temp_cont)
            company_id = self.env.company
            temp_cont = self.temp_cont
            temp_id = self.temp_id
            print("temp_id", type(temp_id))
            ver_name = str(self.ver_name)
            print("ver_name", type(ver_name))
            ver_sub = self.ver_subject
            print("ver_sub", type(ver_sub))
            api_info = self.env['ir.config_parameter'].search(
                [('key', '=', "SendGrid API Key " + company_id.name + "")])
            if not api_info:
                raise UserError(_("It Needs API Key"))
            if api_info.company_id.id == self.env.company.id:
                api_key = api_info.value
            if not api_key and api_key == "":
                raise UserError(_("Your Company Needs an API Key"))
            conn = http.client.HTTPSConnection("api.sendgrid.com")
            print("temp_cont", temp_cont)
            upt_temp_cnt = (temp_cont.replace('"', ''))
            print("upt_temp_cnt", type(upt_temp_cnt))
            payload = "{\"template_id\":\"" + temp_id + "\",\"active\":1,\"name\":\"" + ver_name + "\",\"html_content\":\"" + upt_temp_cnt + "\",\"plain_content\":\"<%body%>\",\"subject\":\"" + ver_sub + "\"}"
            print("pay", payload)
            print("payload", type(payload))
            headers = {
                'authorization': "Bearer " + api_key + "",
                'content-type': "application/json"
            }
            print("head", headers)
            conn.request("POST", "/v3/templates/" + temp_id + "/versions", payload, headers)

            res = conn.getresponse()
            data = res.read()
            print("res1", res)
            print("data1", data)
