import requests
import json

class User():
	# gets all users
	def getUsers(self,vault,q):
		endpoint = 'users?q=' + q
		requestUrl = vault.base_url + endpoint
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.get(requestUrl,headers=headers).json()		
		return r

	# get user
	def getUser(self,vault,userId):
		endpoint = 'users/' + userId
		requestUrl = vault.base_url + endpoint
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.get(requestUrl,headers=headers).json()
		return r

	# get a user webtoken
	def getUserToken(self,vault,userId):
		endpoint = 'users/' + userId + '/webToken'
		requestUrl = vault.base_url + endpoint
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		r = requests.get(requestUrl,headers=headers).json()		
		return r

	# creates a user
	def postUser(self,vault,siteId,userId,fName,lName,email,password):
		endpoint = 'users?siteId='
		requestUrl = vault.base_url + endpoint + siteId
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		payload = {'userId':userId,'firstName':fName,'lastName':lName,'emailaddress':email,'password':password}
		r = requests.post(requestUrl,headers=headers,data=payload).json()
		return r

	# update a user
	def putUser(self,vault,userId,fieldsDict):
		endpoint = 'users/'
		requestUrl = vault.base_url + endpoint + userId
		headers = {'Authorization':'Bearer ' + vault.token.access_token}
		payload = fieldsDict
		r = requests.put(requestUrl,headers=headers,data=payload).json()
		return r