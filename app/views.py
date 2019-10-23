from __future__ import division
from flask import render_template, request, jsonify
import json
import os
from app import app
import xgboost as xgb
import numpy as np
import MySQLdb as mdb
import pandas as pd
import geopandas as gpd
#ReCaptcha
from flask_recaptcha import ReCaptcha

app.config['RECAPTCHA_ENABLED'] = True
app.config['RECAPTCHA_SITE_KEY'] = ""
app.config['RECAPTCHA_SECRET_KEY'] = ""
recaptcha = ReCaptcha(app=app)

@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html",) 

@app.route('/output',methods=['GET', 'POST'])
def cities_output():
    if (not recaptcha.verify()):
    	return render_template("error.html")
    else:
    	# Get input data for ACS models (model 1 and model 2)
		X_bmi = []
		X_bmi.append(int(request.form.get('weight')))
		X_bmi.append(int(request.form.get('height_feet')))
		X_bmi.append(int(request.form.get('height_inch')))
		temp_bmi = (703.0 * X_bmi[0]) / ((X_bmi[1]*12.0+X_bmi[2])*(X_bmi[1]*12.0+X_bmi[2]))

		X = []
		for i in range(0,107): X.append(0)

		if request.form.get('gender')==u'1': X[0]=1
		if request.form.get('lanx')==u'1': X[1]=1
		X[2]=request.form.get('age')
		if request.form.get('hispanic')==u'1': X[3]=1
		if request.form.get('waob')==u'1': X[4]=1
		if request.form.get('selfcare')==u'1': X[5]=1
		if request.form.get('hear')==u'1': X[6]=1
		if request.form.get('vision')==u'1': X[7]=1
		if request.form.get('idpliv')==u'1': X[8]=1
		if request.form.get('ambulatory')==u'1': X[9]=1
		if request.form.get('cognitive')==u'1': X[10]=1
		if request.form.get('marital')==u'1': X[11]=1
		elif request.form.get('marital')==u'2': X[12]=1
		elif request.form.get('marital')==u'3': X[13]=1
		elif request.form.get('marital')==u'4': X[14]=1
		elif request.form.get('marital')==u'5': X[15]=1
		elif request.form.get('marital')==u'6': X[15]=1

		if request.form.get('schl')==u'1': X[16]=1
		elif request.form.get('schl')==u'2': X[17]=1
		elif request.form.get('schl')==u'3': X[18]=1
		elif request.form.get('schl')==u'4': X[19]=1
		elif request.form.get('schl')==u'5': X[20]=1
		elif request.form.get('schl')==u'6': X[21]=1
		elif request.form.get('schl')==u'7': X[22]=1
		elif request.form.get('schl')==u'8': X[23]=1
		elif request.form.get('schl')==u'9': X[24]=1
		elif request.form.get('schl')==u'10': X[25]=1
		elif request.form.get('schl')==u'11': X[26]=1
		elif request.form.get('schl')==u'12': X[27]=1
		elif request.form.get('schl')==u'13': X[28]=1
		elif request.form.get('schl')==u'14': X[29]=1
		elif request.form.get('schl')==u'15': X[30]=1
		elif request.form.get('schl')==u'16': X[31]=1
		elif request.form.get('schl')==u'17': X[32]=1
		elif request.form.get('schl')==u'18': X[33]=1
		elif request.form.get('schl')==u'19': X[34]=1
		elif request.form.get('schl')==u'20': X[35]=1
		elif request.form.get('schl')==u'21': X[36]=1
		elif request.form.get('schl')==u'22': X[37]=1
		elif request.form.get('schl')==u'23': X[38]=1
		elif request.form.get('schl')==u'24': X[39]=1

		if request.form.get('waob')==u'1': X[40]=1
		elif request.form.get('waob')==u'2': X[41]=1
		elif request.form.get('waob')==u'3': X[42]=1
		elif request.form.get('waob')==u'4': X[43]=1
		elif request.form.get('waob')==u'5': X[44]=1
		elif request.form.get('waob')==u'6': X[45]=1
		elif request.form.get('waob')==u'7': X[46]=1
		elif request.form.get('waob')==u'8': X[47]=1

		if request.form.get('race')==u'1': X[48]=1
		elif request.form.get('race')==u'2': X[49]=1
		elif request.form.get('race')==u'3': X[50]=1
		elif request.form.get('race')==u'4': X[51]=1
		elif request.form.get('race')==u'5': X[52]=1
		elif request.form.get('race')==u'6': X[53]=1
		elif request.form.get('race')==u'7': X[54]=1
		elif request.form.get('race')==u'8': X[55]=1
		elif request.form.get('race')==u'9': X[55]=1

		mod1_X=np.array([X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X])

		for i in range(0,9): X.append(0)

		if request.form.get('cow')==u'1': X[107]=1
		elif request.form.get('cow')==u'2': X[108]=1
		elif request.form.get('cow')==u'3': X[109]=1
		elif request.form.get('cow')==u'4': X[110]=1
		elif request.form.get('cow')==u'5': X[111]=1
		elif request.form.get('cow')==u'6': X[112]=1
		elif request.form.get('cow')==u'7': X[113]=1
		elif request.form.get('cow')==u'8': X[114]=1
		elif request.form.get('cow')==u'9': X[115]=1

		mod2_X=np.array([X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X,X])


		for i in range(0,52):
			j=i+55 
			mod1_X[i][j]=1
			mod2_X[i][j]=1

		xg_mod1_x = xgb.DMatrix(data=mod1_X,feature_names=['GENDER', 'LANX', 'AGEP', 'HISPANIC', 'NATIVITY', 'SELFCARE','HEAR', 'VISION', 'IDPLIV', 'AMBULATORY', 'COGNITIVE', 'MAR_1','MAR_2', 'MAR_3', 'MAR_4', 'MAR_5', 'SCHL_1.0', 'SCHL_2.0','SCHL_3.0', 'SCHL_4.0', 'SCHL_5.0', 'SCHL_6.0', 'SCHL_7.0','SCHL_8.0', 'SCHL_9.0', 'SCHL_10.0', 'SCHL_11.0', 'SCHL_12.0','SCHL_13.0', 'SCHL_14.0', 'SCHL_15.0', 'SCHL_16.0', 'SCHL_17.0','SCHL_18.0', 'SCHL_19.0', 'SCHL_20.0', 'SCHL_21.0', 'SCHL_22.0','SCHL_23.0', 'SCHL_24.0', 'WAOB_1', 'WAOB_2', 'WAOB_3', 'WAOB_4','WAOB_5', 'WAOB_6', 'WAOB_7', 'WAOB_8', 'RAC1P_1', 'RAC1P_2','RAC1P_3', 'RAC1P_5', 'RAC1P_6', 'RAC1P_8', 'RAC1P_9', 'PUMA_100','PUMA_200', 'PUMA_300', 'PUMA_301', 'PUMA_302', 'PUMA_303','PUMA_304', 'PUMA_400', 'PUMA_501', 'PUMA_502', 'PUMA_503','PUMA_504', 'PUMA_505', 'PUMA_506', 'PUMA_507', 'PUMA_508','PUMA_701', 'PUMA_702', 'PUMA_703', 'PUMA_704', 'PUMA_1000','PUMA_1300', 'PUMA_1400', 'PUMA_1600', 'PUMA_1900', 'PUMA_1901','PUMA_1902', 'PUMA_2400', 'PUMA_2800', 'PUMA_3301', 'PUMA_3302','PUMA_3303', 'PUMA_3304', 'PUMA_3305', 'PUMA_3306', 'PUMA_3400','PUMA_3500', 'PUMA_3601', 'PUMA_3602', 'PUMA_3603', 'PUMA_3900','PUMA_4000', 'PUMA_4200', 'PUMA_4301', 'PUMA_4302', 'PUMA_4303','PUMA_4500', 'PUMA_4700', 'PUMA_4800', 'PUMA_4901', 'PUMA_4902','PUMA_4903'])
		xg_mod2_x = xgb.DMatrix(data=mod2_X,feature_names=['GENDER', 'LANX', 'AGEP', 'HISPANIC', 'NATIVITY', 'SELFCARE','HEAR', 'VISION', 'IDPLIV', 'AMBULATORY', 'COGNITIVE', 'MAR_1','MAR_2', 'MAR_3', 'MAR_4', 'MAR_5', 'SCHL_1.0', 'SCHL_2.0','SCHL_3.0', 'SCHL_4.0', 'SCHL_5.0', 'SCHL_6.0', 'SCHL_7.0','SCHL_8.0', 'SCHL_9.0', 'SCHL_10.0', 'SCHL_11.0', 'SCHL_12.0','SCHL_13.0', 'SCHL_14.0', 'SCHL_15.0', 'SCHL_16.0', 'SCHL_17.0','SCHL_18.0', 'SCHL_19.0', 'SCHL_20.0', 'SCHL_21.0', 'SCHL_22.0','SCHL_23.0', 'SCHL_24.0', 'WAOB_1', 'WAOB_2', 'WAOB_3', 'WAOB_4','WAOB_5', 'WAOB_6', 'WAOB_7', 'WAOB_8', 'RAC1P_1', 'RAC1P_2','RAC1P_3', 'RAC1P_5', 'RAC1P_6', 'RAC1P_8', 'RAC1P_9', 'PUMA_100','PUMA_200', 'PUMA_300', 'PUMA_301', 'PUMA_302', 'PUMA_303','PUMA_304', 'PUMA_400', 'PUMA_501', 'PUMA_502', 'PUMA_503','PUMA_504', 'PUMA_505', 'PUMA_506', 'PUMA_507', 'PUMA_508','PUMA_701', 'PUMA_702', 'PUMA_703', 'PUMA_704', 'PUMA_1000','PUMA_1300', 'PUMA_1400', 'PUMA_1600', 'PUMA_1900', 'PUMA_1901','PUMA_1902', 'PUMA_2400', 'PUMA_2800', 'PUMA_3301', 'PUMA_3302','PUMA_3303', 'PUMA_3304', 'PUMA_3305', 'PUMA_3306', 'PUMA_3400','PUMA_3500', 'PUMA_3601', 'PUMA_3602', 'PUMA_3603', 'PUMA_3900','PUMA_4000', 'PUMA_4200', 'PUMA_4301', 'PUMA_4302', 'PUMA_4303','PUMA_4500', 'PUMA_4700', 'PUMA_4800', 'PUMA_4901', 'PUMA_4902','PUMA_4903','COW_1.0', 'COW_2.0', 'COW_3.0', 'COW_4.0', 'COW_5.0','COW_6.0', 'COW_7.0', 'COW_8.0', 'COW_9.0'])


		SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
		bst_url1 = os.path.join(SITE_ROOT, "model", "employMA841387.model")
		bst_url2 = os.path.join(SITE_ROOT, "model", "incomeMA43164.model")
		bst_url3 = os.path.join(SITE_ROOT, "model", "healthMA741031.model")


		bst_mod1 = xgb.Booster(model_file=bst_url1)
		bst_mod2 = xgb.Booster(model_file=bst_url2)

		mod1_y = bst_mod1.predict(xg_mod1_x)
		mod2_y = bst_mod2.predict(xg_mod2_x)

		#Get input data for BRFSS model (model 3)

		XB = []
		for i in range(0,51): XB.append(0)

		if request.form.get('exerany2')==u'1': XB[0]=1
		if request.form.get('gender')==u'1': XB[1]=1
		XB[2]=request.form.get('age')
		XB[3]=temp_bmi
		if request.form.get('cvdinfr4')==u'1': XB[4]=1
		if request.form.get('cvdcrhd4')==u'1': XB[5]=1
		if request.form.get('cvdstrk3')==u'1': XB[6]=1
		if request.form.get('asthma3')==u'1': XB[7]=1
		if request.form.get('chcscncr')==u'1': XB[8]=1
		if request.form.get('chcocncr')==u'1': XB[9]=1
		if request.form.get('chccopd1')==u'1': XB[10]=1
		if request.form.get('havarth3')==u'1': XB[11]=1
		if request.form.get('addepev2')==u'1': XB[12]=1
		if request.form.get('chckidny')==u'1': XB[13]=1
		if request.form.get('diabete3')==u'1': XB[14]=1
		if request.form.get('hispanic')==u'1': XB[15]=1
		if request.form.get('qlactlm2')==u'1': XB[16]=1
		if request.form.get('useequip')==u'1': XB[17]=1
		if request.form.get('hlthpln1')==u'1': XB[18]=1
		if request.form.get('race')==u'1': XB[19]=1
		elif request.form.get('race')==u'2': XB[20]=1
		elif ((request.form.get('race')==u'3') or (request.form.get('race')==u'4') or (request.form.get('race')==u'5')): XB[21]=1
		elif request.form.get('race')==u'6': XB[22]=1
		elif request.form.get('race')==u'7': XB[23]=1
		elif request.form.get('race')==u'8': XB[24]=1
		elif request.form.get('race')==u'9': XB[25]=1
		if request.form.get('marital')==u'1': XB[26]=1
		elif request.form.get('marital')==u'3': XB[27]=1
		elif request.form.get('marital')==u'2': XB[28]=1
		elif request.form.get('marital')==u'4': XB[29]=1
		elif request.form.get('marital')==u'5': XB[30]=1
		elif request.form.get('marital')==u'6': XB[31]=1
		if request.form.get('schl') in [u'1',u'2',u'3']: XB[32]=1
		elif request.form.get('schl') in [u'4',u'5',u'6',u'7',u'8',u'9',u'10',u'11']: XB[33]=1
		elif request.form.get('schl') in [u'12',u'13',u'14']: XB[34]=1
		elif request.form.get('schl') in [u'15',u'16',u'17']: XB[35]=1
		elif request.form.get('schl') in [u'18',u'19']: XB[36]=1
		elif request.form.get('schl') in [u'20',u'21',u'22',u'23',u'24']: XB[37]=1
		if request.form.get('_smoker3')==u'1': XB[38]=1
		if request.form.get('_smoker3')==u'2': XB[39]=1
		if request.form.get('_smoker3')==u'3': XB[40]=1
		if request.form.get('_smoker3')==u'4': XB[41]=1

		mod3_X=np.array([XB,XB,XB,XB,XB,XB,XB,XB,XB,XB,XB,XB,XB,XB])

		mod3_X[0][42]=1
		mod3_X[1][45]=1
		mod3_X[2][44]=1
		mod3_X[3][42]=1
		mod3_X[4][44]=1
		mod3_X[5][45]=1
		mod3_X[6][45]=1
		mod3_X[7][45]=1
		mod3_X[8][46]=1
		mod3_X[9][42]=1
		mod3_X[10][47]=1
		mod3_X[11][48]=1
		mod3_X[12][49]=1
		mod3_X[13][50]=1

		xg_mod3_x = xgb.DMatrix(data=mod3_X,feature_names=['EXERANY2', 'SEX', 'AGE', '_BMI5', 'CVDINFR4', 'CVDCRHD4','CVDSTRK3', 'ASTHMA3', 'CHCSCNCR', 'CHCOCNCR', 'CHCCOPD1','HAVARTH3', 'ADDEPEV2', 'CHCKIDNY', 'DIABETE3', 'HISPANC2','QLACTLM2', 'USEEQUIP', 'HLTHPLN1', '_MRACE_1.0', '_MRACE_2.0','_MRACE_3.0', '_MRACE_4.0', '_MRACE_5.0', '_MRACE_6.0','_MRACE_7.0', 'MARITAL_1.0', 'MARITAL_2.0', 'MARITAL_3.0','MARITAL_4.0', 'MARITAL_5.0', 'MARITAL_6.0', 'EDUCA_1.0','EDUCA_2.0', 'EDUCA_3.0', 'EDUCA_4.0', 'EDUCA_5.0', 'EDUCA_6.0','_SMOKER3_1', '_SMOKER3_2', '_SMOKER3_3', '_SMOKER3_4', '_CNTY_1','_CNTY_5', '_CNTY_9', '_CNTY_13', '_CNTY_17', '_CNTY_21','_CNTY_23', '_CNTY_25', '_CNTY_27'])
		bst_mod3 = xgb.Booster(model_file=bst_url3)
		mod3_y = bst_mod3.predict(xg_mod3_x)


		#Join the puma, county, and census tracts
		con = mdb.connect('localhost', 'hui', 'Rong3231;', 'Insight')

		sqlq = 'SELECT * FROM ma_tract_final;'
		tract = pd.read_sql(sql=sqlq,con=con)
		tract['cnty']=(tract.GEOID - tract.GEOID%1000000)/1000000-25000


		PUMA = []
		for puma in set(tract.PUMACE10.values):
			PUMA.append(puma)
		PUMA.sort()

		d = pd.DataFrame({'PUMA':pd.Series(PUMA),'unemploy':mod1_y,'income':mod2_y})
		d2 = pd.DataFrame({'cnty':pd.Series([1,3,5,7,9,11,13,15,17,19,21,23,25,27]),'health':mod3_y})
		tract = tract.merge(right=d,how='left',left_on='PUMACE10',right_on='PUMA')
		tract = tract.merge(right=d2,how='left',left_on='cnty',right_on='cnty')

		#normalizations
		def normalize(x):
			norm_x = (x-x.min())/(x.max()-x.min())
			return norm_x

		tract['norm_unemploy']=normalize(tract.unemploy)
		tract['norm_income']=1-normalize(tract.income)
		tract['norm_health']=normalize(tract.health)
		tract['norm_npark']=normalize(tract.npark)
		tract['norm_ngrocery']=normalize(tract.ngrocery)
		tract['norm_nhospital']=normalize(tract.nhospital)
		tract['norm_ndoctor']=normalize(tract.ndoctor)
		tract['norm_ndisable']=normalize(tract.ndisable)
		tract['norm_nnature']=normalize(tract.nnature)
		tract['norm_nbus']=normalize(tract.nbus)
		tract['norm_npharm']=normalize(tract.npharm)
		tract['norm_nrestaurant']=normalize(tract.nrestaurant)
		tract['norm_nsubway']=normalize(tract.nsubway)
		tract['norm_nzoo']=normalize(tract.nzoo)
		tract['norm_ncomctr']=normalize(tract.ncomctr)
		tract['norm_mhv']=1-normalize(tract.mhv) #1-normalize(tract.mhv)

		weight=[]
		weight.append(int(request.form.get('remploy')))
		weight.append(int(request.form.get('raccess')))
		weight.append(int(request.form.get('rhealth')))
		weight.append(int(request.form.get('rpark')))
		weight.append(int(request.form.get('rgrocery')))
		weight.append(int(request.form.get('rhospital')))
		weight.append(int(request.form.get('rdoctor')))
		weight.append(int(request.form.get('rdisable')))
		weight.append(int(request.form.get('rnature')))
		weight.append(int(request.form.get('rbus')))
		weight.append(int(request.form.get('rpharm')))
		weight.append(int(request.form.get('rrestaurant')))
		weight.append(int(request.form.get('rsubway')))
		weight.append(int(request.form.get('rzoo')))
		weight.append(int(request.form.get('rcomctr')))
		weight.append(int(request.form.get('remploy')))

		tract['norm_afford']=normalize(tract.norm_unemploy+tract.norm_income+tract.norm_mhv)

		tract['access']=weight[3]*tract.norm_npark+weight[4]*tract.norm_ngrocery+weight[5]*tract.norm_nhospital+weight[6]*tract.norm_ndoctor+weight[7]*tract.norm_ndisable+weight[8]*tract.norm_nnature+weight[9]*tract.norm_nbus+weight[10]*tract.norm_npharm+weight[11]*tract.norm_nrestaurant+weight[12]*tract.norm_nsubway+weight[13]*tract.norm_nzoo+weight[14]*tract.norm_ncomctr

		tract['norm_access']=normalize(tract.access)

		tract['score']=weight[0]*tract.norm_afford+weight[2]*tract.norm_health+weight[1]*tract.norm_access

		score_min = tract.score.min()
		score_max = tract.score.max()

		tract['employ'] = 1-tract.unemploy

		tract['norm_score'] = 100*(tract.score-score_min)/(score_max-score_min)
		tract = np.round(tract, decimals=2)

		#merge tract to geojson
		SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
		json_url = os.path.join(SITE_ROOT, "data", "matract.json")
		tractjs = gpd.read_file(json_url)
		tractjs[['GEOID']] = tractjs[['GEOID']].astype(int)
		tractjs = gpd.GeoDataFrame(tract.merge(right=tractjs,how='left',left_on='GEOID',right_on='GEOID'))
		
		tractgeojson = json.loads(tractjs.to_json())

	  	return render_template("map.html", ress = tractgeojson, woutput= weight) 







