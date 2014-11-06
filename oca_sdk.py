import requests
import json
from lxml import etree

# --------------------------------------------------------------------------------------------------

class OCAServerError(Exception):
    pass

class NoDataReturned(Exception):
    pass

class DataTagNotFound(Exception):
    pass

# --------------------------------------------------------------------------------------------------

class OCA(object):
    def __init__(self, cuit):
        self.version = "0.1.0"
        self.__client = self.Client(self)
        self.__cuit = cuit

    def get_text(self, context, tag):
        xml_tag = context.find('.//' + tag)

        if xml_tag is not None:
            if xml_tag.text is not None:
                return '%s' % (xml_tag.text.strip())
            return ''
        else:
            raise DataTagNotFound(tag)

    def get_error_msg(self, **kwargs):
        return ''.join('\n\n %s: \n %s' % (k.upper(), v) for k, v in kwargs.iteritems())

    def findall(self, element, tag, request={}, uri=''):
        nodes = element.findall('.//%s' % tag)
        if not len(nodes):
            msg = self.get_error_msg(uri=uri, request=request, tag=tag)
            raise NoDataReturned(msg)
        return nodes

    def get_province_list(self):
        uri = 'GetProvincias'
        element = self.__client.post(uri)

        provinces = []
        for province in self.findall(element, 'Provincia', {}, uri):
            data = {
                'province_id': self.get_text(province, 'IdProvincia'),
                'description': self.get_text(province, 'Descripcion')
            }
            provinces.append(data)
        return provinces

    def get_district_list_by_province(self, province_id):
        request = {'idProvincia': province_id}
        uri = 'GetLocalidadesByProvincia'
        element = self.__client.post(uri, request)

        districts = []
        for district in self.findall(element, 'Provincia', request, uri):
            data = {'name': self.get_text(district, 'Nombre')}
            districts.append(data)
        return districts

    def get_imposition_center_list(self):
        uri = 'GetCentrosImposicion'
        element = self.__client.post(uri)

        centers = []
        for center in self.findall(element, 'Table', {}, uri):
            data = {
                'center_id': self.get_text(center, 'idCentroImposicion'),
                'code': self.get_text(center, 'Sigla'),
                'street': self.get_text(center, 'Calle'),
                'number': self.get_text(center, 'Numero'),
                'floor': self.get_text(center, 'Piso'),
                'district': self.get_text(center, 'Localidad'),
                'postal_code': self.get_text(center, 'codigopostal'),
            }
            centers.append(data)
        return centers

    def get_imposition_center_list_by_postal_code(self, postal_code):
        request = {'CodigoPostal': postal_code}
        uri = 'GetCentrosImposicionPorCP'
        element = self.__client.post(uri, request)

        centers = []
        for center in self.findall(element, 'Table', request, uri):
            data = {
                'center_id': self.get_text(center, 'idCentroImposicion'),
                'branch_id': self.get_text(center, 'IdSucursalOCA'),
                'code': self.get_text(center, 'Sigla'),
                'street': self.get_text(center, 'Calle'),
                'number': self.get_text(center, 'Numero'),
                'tower': self.get_text(center, 'Torre'),
                'floor': self.get_text(center, 'Piso'),
                'appartment': self.get_text(center, 'Depto'),
                'phone': self.get_text(center, 'Telefono'),
                'district': self.get_text(center, 'Localidad'),
                'province_id': self.get_text(center, 'IdProvincia'),
                'postal_code': self.get_text(center, 'CodigoPostal'),
                'postal_code_id': self.get_text(center, 'idCodigoPostal'),
                'description': self.get_text(center, 'Descripcion')
            }
            centers.append(data)
        return centers

    def get_admission_center_list(self):
        uri = 'GetCentrosImposicionAdmision'
        element = self.__client.post(uri)

        centers = []
        for center in self.findall(element, 'Table', {}, uri):
            data = {
                'center_id': self.get_text(center, 'idCentroImposicion'),
                'code': self.get_text(center, 'Sigla'),
                'street': self.get_text(center, 'Calle'),
                'number': self.get_text(center, 'Numero'),
                'phone': self.get_text(center, 'Telefono'),
                'floor': self.get_text(center, 'Piso'),
                'district': self.get_text(center, 'Localidad'),
                'province': self.get_text(center, 'Provincia'),
                'postal_code': self.get_text(center, 'codigopostal'),
                'description': self.get_text(center, 'Descripcion'),
                'comments': self.get_text(center, 'Observaciones')
            }
            centers.append(data)
        return centers

    def get_admission_center_list_by_postal_code(self, postal_code):
        request = {'CodigoPostal': postal_code}
        uri = 'GetCentrosImposicionAdmisionPorCP'
        element = self.__client.post(uri, request)

        centers = []
        for center in self.findall(element, 'Table', request, uri):
            data = {
                'center_id': self.get_text(center, 'idCentroImposicion'),
                'branch_id': self.get_text(center, 'IdSucursalOCA'),
                'code': self.get_text(center, 'Sigla'),
                'street': self.get_text(center, 'Calle'),
                'number': self.get_text(center, 'Numero'),
                'phone': self.get_text(center, 'Telefono'),
                'floor': self.get_text(center, 'Piso'),
                'tower': self.get_text(center, 'Torre'),
                'district': self.get_text(center, 'Localidad'),
                'postal_code': self.get_text(center, 'CodigoPostal'),
                'postal_code_id': self.get_text(center, 'idCodigoPostal'),
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
        uri = 'Tarifar_Envio_Corporativo'
        element = self.__client.post(uri, request)

        node = element.find('.//Table')
        if node is None:
            msg = self.get_error_msg(uri=uri, request=json.dumps(request))
            raise NoDataReturned(msg)

        return {
            'calculator': self.get_text(node, 'Tarifador'),
            'price': self.get_text(node, 'Precio'),
            'service_id': self.get_text(node, 'idTiposervicio'),
            'area': self.get_text(node, 'Ambito'),
            'eta': self.get_text(node, 'PlazoEntrega'),
            'aditional': self.get_text(node, 'Adicional'),
            'total': self.get_text(node, 'Total')
        }



    def get_shipping_status(self, tracking_number):
        request = {'numeroEnvio': tracking_number}
        uri = 'TrackingEnvio_EstadoActual'
        element = self.__client.post(uri, request)

        if element is None:
            msg = self.get_error_msg(uri=uri, request=request)
            raise NoDataReturned(msg)

        return {
            'tracking_number': self.get_text(element, 'NumeroEnvio'),
            'client_document': self.get_text(element, 'DocumentoCliente'),
            'status': self.get_text(element, 'Estado'),
            'date': self.get_text(element, 'Fecha'),
            'motive': self.get_text(element, 'Motivo'),
            'branch': self.get_text(element, 'Sucursal'),
            'lat': self.get_text(element, 'Latitud'),
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
            root = etree.fromstring(xml, parser=parser)
            if not len(root):
                raise NoDataReturned('Returned XML has no children.')
            return root

        def post(self, uri, data={}):
            result = requests.post(
                self.get_url(uri),
                data=data,
                headers={'User-Agent':self.USER_AGENT}
            )

            if result.status_code != 200:
                msg = self.oca.get_error_msg(
                    http_status=result.status_code, request=json.dumps(data), oca_error=result.text)
                raise OCAServerError(msg)

            return self.parse_xml(result.text)
