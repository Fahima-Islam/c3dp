import numpy as np
import math



class Collimator(object):

    def __init__(self,number_of_chanels= None, front_distance =None,  channel_thickness= None,
                 blade_thickness=None ,acceptanceAngle=None, frontEndDimension = None, bigEndDimension=None, length=None ):

        self.number_of_chanels = number_of_chanels
        self.blade_thickness =blade_thickness
        self.channel_thickness =channel_thickness
        self.acceptanceAngle  = acceptanceAngle
        self.bigEndDimension =bigEndDimension
        self.length = length
        self.front_distance = front_distance
        self.frontEndDimension = frontEndDimension


    def smallEnd_dimension_From_channelNumber(self):
        return ((self.number_of_chanels * self.channel_thickness) + ((self.number_of_chanels + 1) * self.blade_thickness))

    def channelThickness_From_channelNumber(self, frontEndDimension=None ):
        if frontEndDimension is None:
            frontEndDimension =self.frontEndDimension
        return ((frontEndDimension-self.blade_thickness*(self.number_of_chanels+1))/self.number_of_chanels)

    def channelNumber_From_smallEnd_dimension(self):
        return ((self.frontEndDimension-self.blade_thickness)/(self.channel_thickness+self.blade_thickness))

    def smallEnd_Distance_from_center(self):
        return ((self.smallEnd_dimension_From_channelNumber() / 2.) / np.tan(np.deg2rad(self.acceptanceAngle / 2.)))

    def EndDistance_from_dimension( self):
        return ((self.bigEndDimension / 2.) / np.tan(np.deg2rad(self.acceptanceAngle / 2.)))

    def frontDimension_from_frontDistance(self):
        return ( 2.* self.front_distance *np.tan(np.deg2rad(self.acceptanceAngle / 2.)))

    def bigEnd_Dimension_From_length(self):
        return ((self.smallEnd_dimension_From_channelNumber() / self.smallEnd_Distance_from_center()) * (self.smallEnd_Distance_from_center() + self.length))

    def length_From_bigEndDimension(self):
        return( (self.smallEnd_Distance_from_center()*self.bigEndDimension/self.smallEnd_dimension_From_channelNumber()) - self.smallEnd_Distance_from_center())



########################### EXAMPLE ################################################################


# last_section = Collimator(number_of_chanels=27, channel_thickness=3, blade_thickness=1, acceptanceAngle=45,bigEndDimension = 120)
# LastSection_small_end_dimension = last_section.smallEnd_dimension_From_channelNumber()
# print
# print
# print ('last section (big end dimension 120)')
#
# print ('big end distance from center: ', last_section.EndDistance_from_dimension())
# print ('small end dimension; ' ,last_section.smallEnd_dimension_From_channelNumber())
#
# print ('small end distance from center: ' ,last_section.smallEnd_Distance_from_center())
#
# print ('length', last_section.length_From_bigEndDimension())
# print
# print
#
#
#
# middle_section = Collimator (number_of_chanels=9,channel_thickness= 3,blade_thickness=1,acceptanceAngle=45,bigEndDimension =LastSection_small_end_dimension )
#
# middleSection_small_end_dimension = middle_section.smallEnd_dimension_From_channelNumber()
#
# print ('middle_section (bigEndDimension =LastSection_small end dimension = 109)')
#
# print ('small end dimension: ', middle_section.smallEnd_dimension_From_channelNumber())
#
# print ('small end distance from center: ', middle_section.smallEnd_Distance_from_center())
#
# print ('length', middle_section.length_From_bigEndDimension())
#
#
#
#
# print
# print
#
# first_section = Collimator (number_of_chanels=3,channel_thickness= 3,blade_thickness=1,acceptanceAngle= 45,bigEndDimension =middleSection_small_end_dimension)
#
# print ('first section (bigEndDimension=middle Section small end dimension=37)')
#
# print ('small end dimension: ', first_section.smallEnd_dimension_From_channelNumber())
#
# print ('small end distance from center: ', first_section.smallEnd_Distance_from_center())
#
# print ('length', first_section.length_From_bigEndDimension())
# print
# print
#
#
# total_length = last_section.length_From_bigEndDimension() + middle_section.length_From_bigEndDimension() + first_section.length_From_bigEndDimension()
# print ('total length: ', total_length )
#
#
# fd= [22.72, 43.88,54.03, 61.6,74, 76.25, 85.6,
#                                        100.5,120.67,130.5,160.6,180.7]
# h=[]
# for i in fd:
#  collimator =Collimator(front_distance=i, acceptanceAngle=45.)
#  h.append(collimator.frontDimension_from_frontDistance())
#
# for i in h:
#     coll = Collimator (frontEndDimension=i, channel_thickness=3., blade_thickness=1.)
#     print (math.floor(coll.channelNumber_From_smallEnd_dimension()))












