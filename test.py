# -*- coding: utf-8 -*-

__author__ = 'Francisco Perez <francofuji@gmail.com>'

import unittest, datetime

from django.contrib.auth.models import User

from pythie.models import *
from apps.permissions.models import Content_Type_Registration, Right, Content_Object_Right
from apps.permissions.utils import get_right

class PermissionsTestCase(unittest.TestCase):

	def setUp(self):
		'''
		We are creating here an office with two groups and three users. The groups both belong to the same
		office. For the users users two belongs to one group and the third user belongs to the second group.
		There are three possible rights. The first right will be assined to the office, the second right will be
		assigned to a group and the third one will be assigned to the third user.
		'''

		# Set rights
		self.rightA = Right.objects.create(short_name = 'rightA')
		self.rightB = Right.objects.create(short_name = 'rightB')
		self.rightC = Right.objects.create(short_name = 'rightC')

		# Register content types and hierarchy
		Content_Type_Registration.register_content_type((Office,),(Group, Office, 'office'),(UserProfile, Group, 'group'))

		# Create an office
		self.region = Region.objects.create(code='TEST', name="testRegion")
		self.fundtype = FundType.objects.create(code='FT', name='FundType')
		self.importation = Importation.objects.create(region=self.region, fundtype = self.fundtype,
			time=datetime.datetime.now())
		self.office = Office.objects.create(code="A", name="B",
			importation=self.importation, region=self.region )


		# Create groups
		self.groupA = Group.objects.create(name='testgroupA', office = self.office)
		self.groupB = Group.objects.create(name='testgroupB', office = self.office)

		# Create users and update profiles
		self.userA = User.objects.create_user('testuserA', 'testuserA@gmail.com')
		self.userB = User.objects.create_user('testuserB', 'testuserB@gmail.com')
		self.userC = User.objects.create_user('testuserC', 'testuserC@gmail.com')

		self.userprofileA = self.userA.get_profile()
		self.userprofileA.group = self.groupA
		self.userprofileA.save()

		self.userprofileB = self.userB.get_profile()
		self.userprofileB.group = self.groupB
		self.userprofileB.save()

		self.userprofileC = self.userC.get_profile()
		self.userprofileC.group = self.groupB
		self.userprofileC.save()

		# Assigning rights
		rA = Content_Object_Right(content_object = self.office, right = self.rightA)
		rA.save()

		rB = Content_Object_Right(content_object = self.groupB, right = self.rightB)
		rB.save()

		rC = Content_Object_Right(content_object = self.userC.get_profile(), right = self.rightC)
		rC.save()

	def testGetRight(self):
		self.assertEquals(get_right(self.userA.get_profile()), 'rightA') # got it from the office
		self.assertEquals(get_right(self.userB.get_profile()), 'rightB') # got it from the group it belongs
		self.assertEquals(get_right(self.userC.get_profile()), 'rightC') # was directly assigned to user
