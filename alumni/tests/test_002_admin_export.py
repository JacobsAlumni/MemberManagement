from __future__ import annotations
from openpyxl import load_workbook

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from MemberManagement.tests.integration import IntegrationTest

from alumni.models import Alumni
import datetime

EXPECT_EXPORT = [
    ['profile__username', 'eilie', 'Ramila', 'nmal', 'yfeng', 'LiRongTsao', 'Hichat', 'Irew1996', 'Douner', 'Aint1975', 'Mounfem'],
    ['profile__is_staff', False, False, False, False, False, False, False, False, False, True],
    ['profile__is_superuser', False, False, False, False, False, False, False, False, False, True],
    ['profile__date_joined', datetime.datetime(2020, 2, 4, 15, 43, 14, 821001), datetime.datetime(2020, 2, 4, 15, 39, 25, 162000), datetime.datetime(2020, 2, 4, 15, 34, 20, 250000), datetime.datetime(2020, 2, 4, 15, 30, 7, 400001), datetime.datetime(2020, 2, 4, 15, 23, 51, 168000), datetime.datetime(2020, 2, 4, 15, 19, 32, 680000), datetime.datetime(2020, 2, 4, 15, 16, 19, 631000), datetime.datetime(2020, 2, 4, 15, 11, 48, 8000), datetime.datetime(2020, 2, 4, 14, 55, 16, 898000), datetime.datetime(2019, 9, 19, 16, 16, 31, 21999)],
    ['profile__last_login', datetime.datetime(2020, 2, 4, 15, 43, 14, 838000), datetime.datetime(2020, 2, 4, 15, 39, 25, 178999), datetime.datetime(2020, 2, 4, 15, 34, 20, 265000), datetime.datetime(2020, 2, 4, 15, 30, 7, 416001), datetime.datetime(2020, 2, 4, 15, 23, 51, 179000), datetime.datetime(2020, 2, 4, 15, 19, 32, 694000), datetime.datetime(2020, 2, 4, 15, 16, 19, 648999), datetime.datetime(2020, 2, 4, 15, 11, 48, 24000), datetime.datetime(2020, 2, 4, 14, 55, 16, 909000), datetime.datetime(2020, 2, 4, 15, 59, 8, 965000)],
    ['givenName', 'Elena', 'Dharmadhrt', 'Nhoro', 'Yuan', 'Li Rong', 'Mark', 'Krista', 'Karin', 'Klaus', 'Anna'],
    ['middleName', None, None, None, None, None, None, None, None, None, None],
    ['familyName', 'Ilie', 'Ramila', 'Malianga', 'Feng', "Ts'ao", 'Carrasco', 'Hull', 'Daecher', 'Vogt', 'Freytag'],
    ['email', 'Elena@Ilie.ro', 'Dharmadhrt.Ramila@india.com', 'nmal@fancydomain.wtf', 'YuanFeng@teleworm.us', 'LiRongTsao@teleworm.us', 'MarkACarrasco@jourrapide.com', 'KristaCHull@dayrep.com', 'KarinDaecher@rhyta.com', 'KlausVogt@rhyta.com', 'AnnaFreytag@dayrep.com'],
    ['existingEmail', None, None, None, None, None, None, None, None, None, None],
    ['resetExistingEmailPassword', False, False, False, False, False, False, False, False, False, False],
    ['sex', 'fe', 'ma', 'ma', 'fe', 'ma', 'ma', 'fe', 'fe', 'ma', 'fe'],
    ['birthday', datetime.datetime(2000, 6, 6, 0, 0), datetime.datetime(1969, 8, 11, 0, 0), datetime.datetime(1982, 7, 4, 0, 0), datetime.datetime(1993, 2, 18, 0, 0), datetime.datetime(1998, 7, 23, 0, 0), datetime.datetime(1952, 7, 19, 0, 0), datetime.datetime(1996, 4, 14, 0, 0), datetime.datetime(1944, 9, 6, 0, 0), datetime.datetime(1975, 6, 16, 0, 0), datetime.datetime(1948, 11, 7, 0, 0)],
    ['nationality', 'RO', 'IN', 'ZW', 'CN', 'CN', 'US', 'US', 'DE', 'DE', 'DE'],
    ['category', 're', 'fa', 're', 're', 're', 're', 're', 're', 're', 're'],
    ['address__address_line_1', 'Strada General Traian Moșoiu 22', 'Campus Ring 1', '97 Churchill Ave', '513 E 5th St', 'Yangchenghu W Rd', '12345  Counts Ln', '10 Rubaiyat Dr', 'Schillerstrasse 11', 'Leipziger Straße 40', 'Alt-Moabit 72'],
    ['address__address_line_2', None, 'Apt 007', None, None, None, None, None, None, None, None],
    ['address__city', 'Cluj-Napoca', 'Bremen', 'Harare', 'New York City', 'Qingpu', 'Jefferson', 'Los Angeles', 'Wolfratshausen', 'Pegestorf', 'Breunsdorf'], ['address__zip', '400124', '28759', '00263', '10009', '44VG+XR', '24210', '70301', '82515', '37619', '04574'], ['address__state', None, 'Bremen', None, 'New York', 'Shanghai', 'Virgina', 'California', 'Bavaria', None, 'Sachsen'],
    ['address__country', 'RO', 'DE', 'ZW', 'US', 'CN', 'US', 'US', 'DE', 'DE', 'DE'],
    ['social__facebook', None, None, None, None, None, None, None, None, 'https://facebook.com/Aint1975', 'https://facebook.com/anna.freytag'], ['social__linkedin', None, None, None, None, None, None, None, None, None, 'https://www.linkedin.com/in/anna-freytag-1234578'],
    ['social__twitter', None, None, None, None, None, None, None, None, 'https://twitter.com/Aint1975', 'https://twitter.com/anna.freytag'],
    ['social__instagram', None, None, None, None, None, None, None, None, 'https://instagram.com/Aint1975', 'https://instagram.com/anna.freytag'], ['social__homepage', None, None, None, None, None, None, None, None, 'https://Aint1975.com', 'https://anna-freytag.com'],
    ['jacobs__college', 1, 1, 2, 2, 3, 3, 4, 5, 5, 4], ['jacobs__graduation', 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2010, 2009, 2011],
    ['jacobs__degree', 'bsc', 'msc', 'phd', 'ba', 'ba', 'bsc', 'ma', 'msc', 'bsc', 'bsc'],
    ['jacobs__major', 'CS', 'SCEAM', 'PSY', 'IR', 'H', 'BACB', 'IR', 'DE', 'P', 'P'],
    ['jacobs__comments', None, None, None, None, None, None, None, None, None, 'I am not real'],
    ['approval__approval', True, True, True, True, True, True, True, True, True, True],
    ['approval__time', datetime.datetime(2020, 2, 4, 16, 0, 3, 999999), datetime.datetime(2020, 2, 4, 16, 0, 30), datetime.datetime(2020, 2, 4, 16, 0, 53, 1), datetime.datetime(2020, 2, 4, 16, 1, 11), datetime.datetime(2020, 2, 4, 16, 1, 30, 999999), datetime.datetime(2020, 2, 4, 16, 1, 55), datetime.datetime(2020, 2, 4, 16, 2, 4), datetime.datetime(2020, 2, 4, 16, 2, 28, 999999), datetime.datetime(2020, 2, 4, 16, 2, 44), datetime.datetime(2020, 2, 4, 16, 3, 0, 999999)],
    ['approval__gsuite', 'test-e.Ilie@jacobs-alumni.de', 'test-d.ramila@jacobs-alumni.de', 'test-n.malianga@jacobs-alumni.de', 'test-y.feng@jacobs-alumni.de', 'test-l.tsao@jacobs-alumni.de', 'test-m.carrasco@jacobs-alumni.de', 'test-k.hull@jacobs-alumni.de', 'test-k.daecher@jacobs-alumni.de', 'test-k.vogt@jacobs-alumni.de', 'test-a.freytag@jacobs-alumni.de'],
    ['job__employer', 'Fancy Technology Firm', 'Jacobs University Bremen', 'Mr Jones', 'United Nations', 'Antique Car Place', 'Red Robin Stores', 'Quickbiz', "Johnson's General Stores", 'Court Judge Inc', 'Solution Realty'],
    ['job__position', 'Junior Engineer', 'Lecturer', 'Personal Doctor', 'Intern', 'Historian', 'Personnel training officer', 'Researcher', 'Retail Manager', 'General Trial Court Judge', 'Junior Research Engineer'],
    ['job__industry', 4, 69, 139, 74, 53, 54, 107, 27, 73, 114],
    ['job__job', 29, 9, 18, 33, 25, 33, 25, 23, 15, 29],
    ['skills__otherDegrees', None, None, None, None, None, None, None, None, None, 'Bachelor of Computer Science from IUB'], ['skills__spokenLanguages', None, None, None, None, None, None, None, None, None, 'German, English, Spanish'],
    ['skills__programmingLanguages', None, None, None, None, None, None, None, None, None, 'HTML, CSS, JavaScript, Python'],
    ['skills__areasOfInterest', None, None, None, None, None, None, None, None, None, 'Start-Ups, Surfing, Big Data, Human Rights'],
    ['skills__alumniMentor', False, False, False, False, False, False, False, False, False, False],
    ['membership__tier', 'co', 'st', 'co', 'st', 'st', 'st', 'st', 'pa', 'co', 'co'],
    ['membership__desired_tier', None, None, None, None, None, None, None, None, None, None],
    ['atlas__secret', None, None, None, None, None, None, None, None, None, None],
    ['atlas__included', True, True, True, False, True, True, True, False, True, True],
    ['atlas__birthdayVisible', True, True, True, False, False, True, False, False, False, True],
    ['atlas__contactInfoVisible', True, True, True, False, False, True, False, False, False, True],
    ['setup__date', datetime.datetime(2020, 2, 4, 15, 45, 59, 68000), datetime.datetime(2020, 2, 4, 15, 41, 38, 526000), datetime.datetime(2020, 2, 4, 15, 37, 17, 985000), datetime.datetime(2020, 2, 4, 15, 32, 58, 671000), datetime.datetime(2020, 2, 4, 15, 29, 9, 613000), datetime.datetime(2020, 2, 4, 15, 22, 13, 355000), datetime.datetime(2020, 2, 4, 15, 18, 29, 525001), datetime.datetime(2020, 2, 4, 15, 14, 49, 552000), datetime.datetime(2020, 2, 4, 15, 2, 4, 249000), datetime.datetime(2019, 9, 19, 16, 42, 5, 269000)]
]



class AdminExportTest(IntegrationTest, StaticLiveServerTestCase):
    fixtures = ['registry/tests/fixtures/integration.json']
    user = 'Mounfem'

    def test_export(self) -> None:
        self.load_live_url('admin:alumni_alumni_changelist', selector='.app-alumni.model-alumni.change-list')

        # select all elements and 'Export as XSLX' action
        self.find_element('#action-toggle').click()
        select = self.selenium.find_element_by_xpath('//*[@id="changelist-form"]/div[1]/label/select')
        self.select_dropdown(select, 'Export as XSLX')

        # intercept the form download
        xslx_ok, xslx_data = self.get_form_download(select)
        self.assertTrue(xslx_ok, "check that the download succeeds")

        # read a workbook
        from io import BytesIO
        wb = load_workbook(filename = BytesIO(xslx_data))

        # check that we have the alumni sheet
        sheet = wb.worksheets[0]
        self.assertEqual(sheet.title, "alumni_alumni")

        # read the values
        values = [[cell.value for cell in column] for column in sheet.columns]
        wb.close()

        self.assertEqual(len(values), len(EXPECT_EXPORT), "check that the workbook contains the sheet number of columns")
        for (i, (got, expected)) in enumerate(zip(values, EXPECT_EXPORT)):
            self.assertListEqual(got, expected, "check that column {} is correct".format(i))
