import requests
from lxml import etree

# --------------------------------------------------------------------------------------------------

class OCAServerError(Exception):
    pass

class NoDataReturned(Exception):
    pass

class DataKeyNotFound(Exception):
    pass

# --------------------------------------------------------------------------------------------------

class OCA(object):
    def __init__(self, cuit):
        self.version = "0.1.0"
        self.__client = self.Client(self)
        self.__cuit = cuit

    def get_text(self, context, tag):
        tag = context.find('.//' + tag)
        if tag is not None:
            if tag.text is not None:
                return '%s' % (tag.text.strip())
            return ''
        else:
            raise DataKeyNotFound()

    def get_province_list(self):
        element = self.__client.post('GetProvincias')

        provinces = []
        for province in element.findall('.//Provincia'):
            data = {
                'provinceID': self.get_text(province, 'IdProvincia'),
                'description': self.get_text(province, 'Descripcion')
            }
            provinces.append(data)
        return provinces

    def get_district_list_by_province(self, province_id):
        request = {'idProvincia': province_id}
        element = self.__client.post('GetLocalidadesByProvincia', request)

        districts = []
        for district in element.findall('.//Provincia'):
            data = {'name': self.get_text(district, 'Nombre')}
            districts.append(data)
        return districts

    def get_imposition_center_list(self):
        element = self.__client.post('GetCentrosImposicion')

        centers = []
        for center in element.findall('.//Table'):
            data = {
                'centerID': self.get_text(center, 'idCentroImposicion'),
                'code': self.get_text(center, 'Sigla'),
                'street': self.get_text(center, 'Calle'),
                'number': self.get_text(center, 'Numero'),
                'floor': self.get_text(center, 'Piso'),
                'district': self.get_text(center, 'Localidad'),
                'postalCode': self.get_text(center, 'codigopostal'),
            }
            centers.append(data)
        return centers

    def get_imposition_center_list_by_postal_code(self, postal_code):
        request = {'CodigoPostal': postal_code}
        element = self.__client.post('GetCentrosImposicionPorCP', request)

        centers = []
        for center in element.findall('.//Table'):
            data = {
                'centerID': self.get_text(center, 'idCentroImposicion'),
                'branchID': self.get_text(center, 'IdSucursalOCA'),
                'code': self.get_text(center, 'Sigla'),
                'street': self.get_text(center, 'Calle'),
                'number': self.get_text(center, 'Numero'),
                'tower': self.get_text(center, 'Torre'),
                'floor': self.get_text(center, 'Piso'),
                'appartment': self.get_text(center, 'Depto'),
                'phone': self.get_text(center, 'Telefono'),
                'district': self.get_text(center, 'Localidad'),
                'provinceID': self.get_text(center, 'IdProvincia'),
                'postalCode': self.get_text(center, 'CodigoPostal'),
                'postalCodeID': self.get_text(center, 'idCodigoPostal'),
                'description': self.get_text(center, 'Descripcion')
            }
            centers.append(data)
        return centers

    def get_admission_center_list(self):
        element = self.__client.post('GetCentrosImposicionAdmision')

        centers = []
        for center in element.findall('.//Table'):
            data = {
                'centerID': self.get_text(center, 'idCentroImposicion'),
                'code': self.get_text(center, 'Sigla'),
                'street': self.get_text(center, 'Calle'),
                'number': self.get_text(center, 'Numero'),
                'phone': self.get_text(center, 'Telefono'),
                'floor': self.get_text(center, 'Piso'),
                'district': self.get_text(center, 'Localidad'),
                'province': self.get_text(center, 'Provincia'),
                'postalCode': self.get_text(center, 'codigopostal'),
                'description': self.get_text(center, 'Descripcion'),
                'comments': self.get_text(center, 'Observaciones')
            }
            centers.append(data)
        return centers

    def get_admission_center_list_by_postal_code(self, postal_code):
        request = {'CodigoPostal': postal_code}
        element = self.__client.post('GetCentrosImposicionAdmisionPorCP', request)

        centers = []
        for center in element.findall('.//Table'):
            data = {
                'centerID': self.get_text(center, 'idCentroImposicion'),
                'branchID': self.get_text(center, 'IdSucursalOCA'),
                'code': self.get_text(center, 'Sigla'),
                'street': self.get_text(center, 'Calle'),
                'number': self.get_text(center, 'Numero'),
                'phone': self.get_text(center, 'Telefono'),
                'floor': self.get_text(center, 'Piso'),
                'tower': self.get_text(center, 'Torre'),
                'district': self.get_text(center, 'Localidad'),
                'postalCode': self.get_text(center, 'CodigoPostal'),
                'postalCodeID': self.get_text(center, 'idCodigoPostal'),
                'description': self.get_text(center, 'Descripcion'),
                'comments': self.get_text(center, 'Observaciones')
            }
            centers.append(data)
        return centers

    def get_shipping_cost(self, **kwargs):
        request = {
            'Operativa': kwargs['operative'],
            'PesoTotal': kwargs['weight'],
            'VolumenTotal': kwargs['volume'],
            'CodigoPostalOrigen': kwargs['postal_code_from'],
            'CodigoPostalDestino': kwargs['postal_code_to'],
            'CantidadPaquetes': kwargs['package_count'],
            'Cuit': self.__cuit,
        }
        element = self.__client.post('Tarifar_Envio_Corporativo', request)

        return {
            'calculator': self.get_text(element, 'Tarifador'),
            'price': self.get_text(element, 'Precio'),
            'serviceID': self.get_text(element, 'idTiposervicio'),
            'area': self.get_text(element, 'Ambito'),
            'eta': self.get_text(element, 'PlazoEntrega'),
            'aditional': self.get_text(element, 'Adicional'),
            'total': self.get_text(element, 'Total')
        }

    def get_shipping_status(self, tracking_number):
        request = {'numeroEnvio': tracking_number}
        element = self.__client.post('TrackingEnvio_EstadoActual', request)

        return {
            'trackingNumber': self.get_text(element, 'NumeroEnvio'),
            'clientDocument': self.get_text(element, 'DocumentoCliente'),
            'status': self.get_text(element, 'Estado'),
            'date': self.get_text(element, 'Fecha'),
            'motive': self.get_text(element, 'Motivo'),
            'branch': self.get_text(element, 'Sucursal'),
            'lat': self.get_text(element, 'Latitug'),
            'lng': self.get_text(element, 'Longitud')
        }

    # ----------------------------------------------------------------------------------------------

    class Client(object):
        API_BASE_URL = 'http://webservice.oca.com.ar/oep_tracking/Oep_Track.asmx/'

        def __init__(self, oca):
            self.oca = oca
            self.USER_AGENT = 'OCA Python SDK v%s' % (self.oca.version)


        def get_url(self, uri):
            return self.API_BASE_URL + uri

        def parse_xml(self, xml):
            xml = xml.encode('utf-8')
            parser = etree.XMLParser(
                ns_clean=True,
                recover=True,
                encoding='utf-8'
            )
            xml_etree = etree.fromstring(xml, parser=parser)
            if xml_etree is None:
                raise NoDataReturned()
            return xml_etree

        def post(self, uri, data=None):
            result = requests.post(
                self.get_url(uri),
                data=data,
                headers={'User-Agent':self.USER_AGENT}
            )

            if result.status_code != 200:
                raise OCAServerError()
            return self.parse_xml(result.text)
