from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)

class TrackingPackages(models.Model):
    _name = 'tracking.packages'
    _description = 'Tracking Packages'

    tracking_number = fields.Char(string='Tracking Number', required=True)
    status = fields.Char(string='Status')
    carrier = fields.Char(string='Carrier')
    created_date = fields.Datetime(string='Created Date', default=fields.Datetime.now)

    def track_shipment(self, tracking_number):
        url = f'https://api.dhl.com/myshipment/tracking/{tracking_number}'
        
        headers = {
            'Authorization': 'Bearer API_TOKEN',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                shipment_info = response.json() 
                
                self.create({
                    'tracking_number': tracking_number,
                    'status': shipment_info.get('status', 'Unknown'),
                    'carrier': shipment_info.get('carrier', 'DHL'),
                })
                
                _logger.info("Shipment Tracking Information: %s", shipment_info)
                return shipment_info  
            else:
                _logger.error("Error: Received status code %s", response.status_code)
                _logger.error("Error : ", response.text)
                return None  

        except requests.exceptions.RequestException as req_err:
            _logger.error("Request error occurred: %s", req_err)
        except Exception as err:
            _logger.error("An error occurred: %s", err)
