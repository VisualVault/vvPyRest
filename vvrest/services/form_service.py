import requests
import json

class FormService():
	# get all form templates
	def getAllFormTemplates(self,vault,q):
		if len(q) > 0:
			endpoint = 'formtemplates?q=' + q
		else:
			endpoint = 'formtemplates'
		requestUrl = vault.base_url + endpoint
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.get(requestUrl,headers=headers).json()
		return r

	# get form template by id
	def getFormTemplateId(self,vault,formId):
		endpoint = 'formtemplates/' + formId
		requestUrl = vault.base_url + endpoint
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.get(requestUrl,headers=headers).json()
		return r

	# get form template form
	def getFormTemplateForm(self,vault,templateId,formId,qs):
		endpoint = 'formtemplates/' + templateId + '/forms/' + formId + '?' + qs
		requestUrl = vault.base_url + endpoint
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.get(requestUrl,headers=headers).json()
		return r

	# get form instance pdf
	def getFormPDF(self,vault,templateId,formId,filePath):
		endpoint = 'formtemplates/' + templateId + '/forms/' + formId + '/PDF'
		requestUrl = vault.base_url + endpoint
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.get(requestUrl,headers=headers,stream=True)	
		file = open(filePath,'wb')
		data = r.raw.read()
		file.write(data)	
		return r

	# get form template fields by id
	def getFormTemplateFields(self,vault,formId):
		endpoint = 'formtemplates/' + formId + '/fields'
		requestUrl = vault.base_url + endpoint
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.get(requestUrl,headers=headers).json()
		return r

	# get form instances of a form template
	def getFormInstances(self,vault,formId,qs):
		endpoint = 'formtemplates/' + formId + '/forms?' + qs
		requestUrl = vault.base_url + endpoint
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.get(requestUrl,headers=headers).json()
		return r

	# get form instances of a form template by search
	def getFormInstancesBySearch(self,vault,formId,q):
		endpoint = 'formtemplates/' + formId + '/forms?q=' + q
		requestUrl = vault.base_url + endpoint
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.get(requestUrl,headers=headers).json()
		return r

	# fill in a form
	def postForm(self,vault,id,fieldsDict):
		endpoint = 'formtemplates/' + id + '/forms'
		requestUrl = vault.base_url + endpoint
		fields = fieldsDict
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.post(requestUrl,headers=headers,data=fields).json()
		return r

	# fill in a revision of existing form
	def postRevForm(self,vault,id,revId,fieldsDict):
		endpoint = 'formtemplates/' + id + '/forms/' + revId
		requestUrl = vault.base_url + endpoint
		fields = fieldsDict
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.post(requestUrl,headers=headers,data=fields).json()
		return r

	# relate form to form
	def relateForm(self,vault,form1,form2):
		endpoint = 'forminstance/' + form1 + '/relateform?relatetoid=' + form2
		requestUrl = vault.base_url + endpoint
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.put(requestUrl,headers=headers).json()
		return r

	# relate form to doc
	def relateDoc(self,vault,formId,docId):
		endpoint = 'forminstance/' + formId + '/relatedocument?relatetoid=' + docId
		requestUrl = vault.base_url + endpoint
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.put(requestUrl,headers=headers).json()
		return r

	# relate form to project
	def relateProject(self,vault,formId,projectId):
		endpoint = 'forminstance/' + formId + '/relateproject?relatetoid=' + projectId
		requestUrl = vault.base_url + endpoint
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.put(requestUrl,headers=headers).json()
		return r

	# unrelate form to form
	def unrelateForm(self,vault,form1,form2):
		endpoint = 'forminstance/' + form1 + '/unrelateform?relatetoid=' + form2
		requestUrl = vault.base_url + endpoint
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.put(requestUrl,headers=headers).json()
		return r

	# unrelate form to doc
	def unrelateDoc(self,vault,formId,docId):
		endpoint = 'forminstance/' + formId + '/unrelatedocument?relatetoid=' + docId
		requestUrl = vault.base_url + endpoint
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.put(requestUrl,headers=headers).json()
		return r

	# unrelate form to project
	def unrelateProject(self,vault,formId,projectId):
		endpoint = 'forminstance/' + formId + '/unrelateproject?relatetoid=' + projectId
		requestUrl = vault.base_url + endpoint
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.put(requestUrl,headers=headers).json()
		return r

	# embedded form url
	def embedForm(self,vault,webToken,formId):
		login = vault.url + '/vvlogin?token=' + webToken
		returnUrl = '&returnUrl=~%2fFormDetails%3fformid%3d' + formId + '%26hidemenu%3Dtrue'
		request = login + returnUrl
		return request

	# get related docs
	def getRelatedDocs(self,vault,formId,qs):
		endpoint = 'forminstance/' + formId + "/documents?" + qs
		requestUrl = vault.base_url + endpoint
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.get(requestUrl,headers=headers).json()
		return r

	# get related forms
	def getRelatedForms(self,vault,formId,qs):
		endpoint = 'forminstance/' + formId + "/forms?" + qs
		requestUrl = vault.base_url + endpoint
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.get(requestUrl,headers=headers).json()
		return r