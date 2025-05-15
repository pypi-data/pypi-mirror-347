# -*- coding: utf-8 -*-
from mongoengine import *
from mongoengine.fields import DateTimeField, EmbeddedDocumentField, FloatField, IntField, StringField, ListField
from fmconsult.database.models.base import CustomBaseDocument
from .dataexplained import DataExplained
from datetime import datetime

class Record(CustomBaseDocument):
	meta = {'collection': 'records'}

	data = DateTimeField(primary_key=True, required=True, index=True)
	alimentacao = IntField()
	can_fl = FloatField()
	can_gear = StringField()
	can_hor = StringField() 
	can_idle_time = FloatField()
	can_mov_time = FloatField()
	can_odometer = FloatField()
	can_rpm = FloatField()
	can_temp = FloatField()
	can_top_speed = FloatField()
	can_travel_time = FloatField() 
	can_v = FloatField()
	data_gps = EmbeddedDocumentField(DataExplained)
	direcao = IntField()
	entradas = StringField()
	eventos = ListField(IntField())
	gpsfix = IntField() 
	ibutton = StringField()
	id_veiculo = IntField()
	cliente_id = IntField()
	cliente_nome = StringField()
	ignicao = IntField()
	lat = FloatField()
	lon = FloatField()
	motorista = StringField() 
	nivel_bateria_reserva = FloatField() 
	bat_carreg = StringField()
	bat_fail = StringField()
	bat_percent = FloatField()
	panico = IntField()
	saidas = StringField()
	sequencia = StringField()
	tensao_bateria = FloatField() 
	timestamp = DateTimeField()
	tipotrans = StringField()
	veiculo = StringField() 
	velocidade = IntField()
	volts = FloatField() 
	voltsbkp = FloatField() 
	num_sat = IntField()
	antifurto = StringField()
	rpm = IntField()
	accel_eve = IntField()
	odometro = IntField()
	low_power = StringField() 
	accel_stat = StringField() 
	horimetro = StringField()
	accel_val = IntField()
	temper = IntField()
	nivel_combustivel = FloatField()
	temperatura = FloatField()
	altitude = FloatField()
	modulo = StringField()
	  
	def to_json(self):
		def format_datetime(dt):
			return dt.isoformat() if isinstance(dt, datetime) else dt

		data_dict = {
			"alimentacao": self.alimentacao,
			"can_fl": self.can_fl,
			"can_gear": self.can_gear,
			"can_hor": self.can_hor,
			"can_idle_time": self.can_idle_time,
			"can_mov_time": self.can_mov_time,
			"can_odometer": self.can_odometer,
			"can_rpm": self.can_rpm,
			"can_temp": self.can_temp,
			"can_top_speed": self.can_top_speed,
			"can_travel_time": self.can_travel_time,
			"can_v": self.can_v,
			"data": format_datetime(self.data),
			"data_gps": {
				"date": self.data_gps.date,
				"timezone": self.data_gps.timezone,
				"timezone_type": self.data_gps.timezone_type,
         	},
			"direcao": self.direcao,
			"entradas": self.entradas,
			"eventos": self.eventos,
			"gpsfix": self.gpsfix,
			"ibutton": self.ibutton,
			"id_veiculo": self.id_veiculo,
			"cliente_id": self.cliente_id,
			"cliente_nome": self.cliente_nome,
			"ignicao": self.ignicao,
			"lat": self.lat,
			"lon": self.lon,
			"motorista": self.motorista,
			"nivel_bateria_reserva": self.nivel_bateria_reserva,
			"bat_carreg": self.bat_carreg,
			"bat_fail": self.bat_fail,
			"bat_percent": self.bat_percent,
			"panico": self.panico,
			"saidas": self.saidas,
			"sequencia": self.sequencia,
			"tensao_bateria": self.tensao_bateria,
			"timestamp": format_datetime(self.timestamp),
			"tipotrans": self.tipotrans,
			"veiculo": self.veiculo,
			"velocidade": self.velocidade,
			"volts": self.volts,
			"voltsbkp": self.voltsbkp,
			"num_sat": self.num_sat,
			"antifurto": self.antifurto,
			"rpm": self.rpm,
			"accel_eve": self.accel_eve,
			"odometro": self.odometro,
			"low_power": self.low_power,
			"accel_stat": self.accel_stat,
			"horimetro": self.horimetro,
			"accel_val": self.accel_val,
			"temper": self.temper,
			"modulo": self.modulo,
			"created_at": self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
			"updated_at": self.updated_at.strftime('%Y-%m-%d %H:%M:%S') if self.updated_at else None
		}
		
		return data_dict