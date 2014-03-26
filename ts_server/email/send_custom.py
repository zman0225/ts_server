#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: ziyuanliu
# @Date:   2014-03-26 08:10:12
# @Last Modified by:   ziyuanliu
# @Last Modified time: 2014-03-26 08:36:39

import requests

html = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <title>*|MC:SUBJECT|*</title>
		
    <style type="text/css">
		#outlook a{
			padding:0;
		}
		body{
			width:100% !important;
		}
		.ReadMsgBody{
			width:100%;
		}
		.ExternalClass{
			width:100%;
		}
		body{
			-webkit-text-size-adjust:none;
		}
		a span,a .yshortcuts{
			background:none !important;
			border-bottom:none !important;
		}
		body{
			margin:0;
			padding:0;
		}
		img{
			border:0;
			height:auto;
			line-height:100%;
			outline:none;
			text-decoration:none;
		}
		table td{
			border-collapse:collapse;
			mso-table-lspace:0pt;
			mso-table-rspace:0pt;
		}
		#bodyTable{
			height:100% !important;
			margin:0;
			padding:0;
			width:100% !important;
		}
		body,#bodyTable{
			background-color:#302F33;
			background-image:url('http://cdn-images.mailchimp.com/template_images/gallery/bg_supperclub_chalkboard.jpg');
			background-position:top center;
			background-repeat:no-repeat;
		}
		#templateContainer{
			border-right:10px solid #ECECEC;
			border-left:10px solid #ECECEC;
		}
		h1{
			color:#AB6401 !important;
			display:block;
			font-family:Georgia;
			font-size:24px;
			font-style:normal;
			font-weight:bold;
			line-height:100%;
			letter-spacing:1px;
			margin-top:0;
			margin-right:0;
			margin-bottom:10px;
			margin-left:0;
			text-align:center;
		}
		h2{
			color:#AB6401 !important;
			display:block;
			font-family:Georgia;
			font-size:20px;
			font-style:italic;
			font-weight:normal;
			line-height:100%;
			letter-spacing:normal;
			margin-top:0;
			margin-right:0;
			margin-bottom:10px;
			margin-left:0;
			text-align:center;
		}
		h3{
			color:#363439 !important;
			display:block;
			font-family:Georgia;
			font-size:16px;
			font-style:normal;
			font-weight:bold;
			line-height:100%;
			letter-spacing:1px;
			margin-top:0;
			margin-right:0;
			margin-bottom:10px;
			margin-left:0;
			text-align:center;
		}
		h4{
			color:#AB6401 !important;
			display:block;
			font-family:Georgia;
			font-size:14px;
			font-style:normal;
			font-weight:bold;
			line-height:100%;
			letter-spacing:normal;
			margin-top:0;
			margin-right:0;
			margin-bottom:10px;
			margin-left:0;
			text-align:center;
		}
		.preheaderContent{
			color:#FFFFFF;
			font-family:Georgia;
			font-size:10px;
			line-height:125%;
			text-align:left;
		}
		.preheaderContent a:link,.preheaderContent a:visited,.preheaderContent a .yshortcuts {
			color:#FFFFFF;
			font-weight:normal;
			text-decoration:underline;
		}
		#templateHeader{
			background-color:#FFFFFF;
		}
		.templateRibbonBackground{
			background-color:#FFFFFF;
		}
		.templateRibbonContent{
			color:#363439;
			font-family:Georgia;
			font-size:16px;
			font-style:normal;
			font-weight:bold;
			line-height:150%;
			letter-spacing:2px;
			text-align:center;
		}
		.templateRibbonContent a:link .templateRibbonContent a:visited,.templateRibbonContent a .yshortcuts {
			color:#AB6401;
			font-weight:normal;
			text-decoration:underline;
		}
		.headerContent{
			border:1px solid #AAAAAA;
			color:#363439;
			font-family:Helvetica;
			font-size:20px;
			font-weight:bold;
			line-height:100%;
			text-align:left;
			vertical-align:middle;
		}
		.headerContent a:link,.headerContent a:visited,.headerContent a .yshortcuts {
			color:#AB6401;
			font-weight:normal;
			text-decoration:underline;
		}
		#headerImage{
			height:auto;
			max-width:550px !important;
		}
		#templateBody{
			background-color:#FFFFFF;
		}
		.bodyContent{
			color:#363439;
			font-family:Georgia;
			font-size:16px;
			line-height:175%;
			text-align:left;
		}
		.bodyContent a:link,.bodyContent a:visited,.bodyContent a .yshortcuts {
			color:#AB6401;
			font-weight:normal;
			text-decoration:underline;
		}
		.templateButton{
			-moz-border-radius:5px;
			-webkit-border-radius:5px;
			background-color:#B16E12;
			border:0;
			border-radius:5px;
		}
		.templateButtonContent,.templateButtonContent a:link,.templateButtonContent a:visited,.templateButtonContent a .yshortcuts {
			color:#FFFFFF;
			font-family:Georgia;
			font-size:15px;
			font-weight:normal;
			letter-spacing:normal;
			line-height:100%;
			text-align:center;
			text-decoration:none;
		}
		.sidebarBorder{
			border-left:1px solid #DDDDDD;
		}
		.sidebarContent{
			color:#AB6401;
			font-family:Georgia;
			font-size:14px;
			line-height:125%;
			text-align:left;
		}
		.sidebarContent a:link,.sidebarContent a:visited,.sidebarContent a span,.sidebarContent a .yshortcuts {
			color:#AB6401;
			font-weight:normal;
			text-decoration:underline;
		}
		.sidebarContent img{
			display:inline;
			height:auto;
			max-width:150px !important;
		}
		.leftColumnContent{
			color:#434246;
			font-family:Georgia;
			font-size:14px;
			line-height:125%;
			text-align:left;
		}
		.leftColumnContent a:link,.leftColumnContent a:visited,.leftColumnContent a .yshortcuts {
			color:#AB6401;
			font-weight:normal;
			text-decoration:underline;
		}
		.rightColumnContent{
			color:#434246;
			font-family:Georgia;
			font-size:14px;
			line-height:125%;
			text-align:left;
		}
		.rightColumnContent a:link,.rightColumnContent a:visited,.rightColumnContent a .yshortcuts {
			color:#AB6401;
			font-weight:normal;
			text-decoration:underline;
		}
		.leftColumnContent img,.rightColumnContent img{
			display:inline;
			height:auto;
			max-width:260px !important;
		}
		.footerContent{
			color:#FFFFFF;
			font-family:Georgia;
			font-size:10px;
			line-height:150%;
			text-align:center;
		}
		.footerContent a:link,.footerContent a:visited,.footerContent a .yshortcuts,.footerContent a span {
			color:#FFFFFF;
			font-weight:normal;
			text-decoration:underline;
		}
		.footerContent img{
			display:inline;
		}
		#monkeyRewards img{
			max-width:190px;
		}
</style></head>
    <body leftmargin="0" marginwidth="0" topmargin="0" marginheight="0" offset="0" style="-webkit-text-size-adjust: none;margin: 0;padding: 0;background-color: #302F33;background-image: url(http://cdn-images.mailchimp.com/template_images/gallery/bg_supperclub_chalkboard.jpg);background-position: top center;background-repeat: no-repeat;width: 100% !important;">
    	<center>
        	<table border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable" style="margin: 0;padding: 0;background-color: #302F33;background-image: url(http://cdn-images.mailchimp.com/template_images/gallery/bg_supperclub_chalkboard.jpg);background-position: top center;background-repeat: no-repeat;height: 100% !important;width: 100% !important;">
                <tr>
                    <td align="center" valign="top" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                        <!-- // BEGIN PREHEADER -->
                        <table border="0" cellpadding="10" cellspacing="0" width="100%" id="templatePreheader">
                            <tr>
                                <td align="center" valign="top" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                    <table border="0" cellpadding="0" cellspacing="0" width="600">
                                        <tr>
                                            <td valign="top" class="preheaderContent" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;color: #FFFFFF;font-family: Georgia;font-size: 10px;line-height: 125%;text-align: left;">
                                                Use this area to offer a short teaser of your email's content. Text here will show in the preview area of some email clients.
                                            </td>
                                            <!-- *|IFNOT:ARCHIVE_PAGE|* -->
                                            <td valign="top" width="220" class="preheaderContent" style="padding-left: 20px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;color: #FFFFFF;font-family: Georgia;font-size: 10px;line-height: 125%;text-align: left;">
                                                Email not displaying correctly?<br><a href="*|ARCHIVE|*" target="_blank" style="color: #FFFFFF;font-weight: normal;text-decoration: underline;">View it in your browser</a>.
                                            </td>
                                            <!-- *|END:IF|* -->
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                        <!-- END PREHEADER \\ -->
                    </td>
                </tr>
            	<tr>
                	<td align="center" valign="top" style="padding-top: 20px;padding-bottom: 20px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                    	<table border="0" cellpadding="0" cellspacing="0" width="620">
                        	<tr>
                            	<td align="center" valign="top" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                	<table border="0" cellpadding="0" cellspacing="0" width="226">
                                    	<tr>
                                        	<td align="center" valign="top" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                                <img src="http://cdn-images.mailchimp.com/template_images/gallery/ee_plate_top.png" height="65" width="226" style="display: block;border: 0;height: auto;line-height: 100%;outline: none;text-decoration: none;">
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        	<tr>
                            	<td align="center" valign="top" style="background-color: #ECECEC;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                	<table border="0" cellpadding="0" cellspacing="0" width="226">
                                    	<tr>
                                        	<td align="center" valign="bottom" style="background-color: #ECECEC;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                                <img src="http://cdn-images.mailchimp.com/template_images/gallery/ee_plate_outer_middle.png" height="10" width="226" style="display: block;border: 0;height: auto;line-height: 100%;outline: none;text-decoration: none;">
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    	<!-- // BEGIN CONTAINER -->
                        <table border="0" cellpadding="0" cellspacing="0" width="620" id="templateContainer" style="border-right: 10px solid #ECECEC;border-left: 10px solid #ECECEC;">
                        	<tr>
                            	<td align="center" valign="top" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                	<!-- // BEGIN HEADER -->
                                	<table border="0" cellpadding="0" cellspacing="0" width="100%" id="templateHeader" style="background-color: #FFFFFF;">
                                    	<tr>
                                        	<td align="center" valign="top" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                            	<table border="0" cellpadding="0" cellspacing="0" width="226">
                                                	<tr>
                                                    	<td align="center" valign="top" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
			                                            	<img src="http://cdn-images.mailchimp.com/template_images/gallery/ee_plate_inner_middle.png" height="32" width="226" style="display: block;border: 0;height: auto;line-height: 100%;outline: none;text-decoration: none;">
                                                		</td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                        	<td align="center" valign="top" style="padding-bottom: 6px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                                <table border="0" cellpadding="0" cellspacing="0">
                                                    <tr>
                                                        <td align="left" valign="bottom" width="40" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                                        	<table border="0" cellpadding="0" cellspacing="0" width="40" class="templateRibbonBackground" style="border-top: 3px solid #363439;border-bottom: 3px solid #363439;background-color: #FFFFFF;">
                                                            	<tr>
                                                                	<td align="left" valign="bottom" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                                           				<img src="http://cdn-images.mailchimp.com/template_images/gallery/ee_ribbon_inverse_left.png" height="54" width="20" style="display: block;border: 0;height: auto;line-height: 100%;outline: none;text-decoration: none;">
                                                            		</td>
                                                                	<td width="20" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                                                    	<br>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                        <td align="center" valign="bottom" width="" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                                            <table border="0" cellpadding="0" cellspacing="0">
                                                                <tr>
                                                                    <td align="center" colspan="3" valign="bottom" width="" style="border: 3px solid #363439;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                                                        <table border="0" cellpadding="5" cellspacing="0" width="100%" class="templateRibbonBackground" style="background-color: #FFFFFF;">
                                                                            <tr>
                                                                                <td valign="middle" class="templateRibbonContent" style="padding-right: 10px;padding-left: 10px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;color: #363439;font-family: Georgia;font-size: 16px;font-style: normal;font-weight: bold;line-height: 150%;letter-spacing: 2px;text-align: center;">TIME SAVOR&#39;S&nbsp;
<h1 style="display: block;font-family: Georgia;font-size: 24px;font-style: normal;font-weight: bold;line-height: 100%;letter-spacing: 1px;margin-top: 0;margin-right: 0;margin-bottom: 10px;margin-left: 0;text-align: center;color: #AB6401 !important;">NEW WEBSITE UPDATES</h1>
</td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td align="left" valign="bottom" width="15" class="templateRibbonBackground" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;background-color: #FFFFFF;">
                                                                        <img src="http://cdn-images.mailchimp.com/template_images/gallery/ee_ribbon_inverse_left_lower.png" height="14" width="15" style="display: block;border: 0;height: auto;line-height: 100%;outline: none;text-decoration: none;">
                                                                    </td>
                                                                    <td align="center" valign="top" width="100%" class="templateRibbonBackground" style="line-height: 0;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;background-color: #FFFFFF;">
                                                                    	&nbsp;                                                                    	
                                                                    </td>
                                                                    <td align="right" valign="bottom" width="15" class="templateRibbonBackground" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;background-color: #FFFFFF;">
                                                                        <img src="http://cdn-images.mailchimp.com/template_images/gallery/ee_ribbon_inverse_right_lower.png" height="14" width="15" style="display: block;border: 0;height: auto;line-height: 100%;outline: none;text-decoration: none;">
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                        <td align="right" valign="bottom" width="40" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                                        	<table border="0" cellpadding="0" cellspacing="0" width="40" class="templateRibbonBackground" style="border-top: 3px solid #363439;border-bottom: 3px solid #363439;background-color: #FFFFFF;">
                                                            	<tr>
                                                                	<td width="20" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                                                    	<br>
                                                                    </td>
                                                                	<td align="right" valign="bottom" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                                           				<img src="http://cdn-images.mailchimp.com/template_images/gallery/ee_ribbon_inverse_right.png" height="54" width="20" style="display: block;border: 0;height: auto;line-height: 100%;outline: none;text-decoration: none;">
                                                            		</td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    	<tr>
                                        	<td align="center" valign="top" style="padding-bottom: 6px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                            	<table border="0" cellpadding="14" cellspacing="0" width="100%">
                                                	<tr>
                                                    	<td align="center" valign="top" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                                            <table border="0" cellpadding="10" cellspacing="0">
                                                                <tr>
                                                                    <td class="headerContent" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;border: 1px solid #AAAAAA;color: #363439;font-family: Helvetica;font-size: 20px;font-weight: bold;line-height: 100%;text-align: left;vertical-align: middle;">
                                                                        <img src="http://cdn-images.mailchimp.com/template_images/gallery/ee_header_image_spices.jpg" alt="" border="0" style="margin: 0;padding: 0;max-width: 550px;border: 0;height: auto;line-height: 100%;outline: none;text-decoration: none;" id="campaign-icon">
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                    <!-- END HEADER \\ -->
                                </td>
                            </tr>
                        	<tr>
                            	<td align="center" valign="top" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                	<!-- // BEGIN BODY -->
                                	<table border="0" cellpadding="20" cellspacing="0" width="100%" id="templateBody" style="background-color: #FFFFFF;">
                                    	<tr>
                                        	<td align="center" valign="top" style="padding-top: 0;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                            	<table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                	<tr>
                                                        <td align="center" valign="top" width="100%" style="padding-right: 20px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                                <tr>
                                                                    <td valign="top" class="bodyContent" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;color: #363439;font-family: Georgia;font-size: 16px;line-height: 175%;text-align: left;"></td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                        <td align="center" valign="top" width="110" class="sidebarBorder" style="padding-left: 10px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;border-left: 1px solid #DDDDDD;">
                                                            <table border="0" cellpadding="0" cellspacing="0" width="100">
                                                                <tr>
                                                                    <td valign="top" class="sidebarContent" style="padding-top: 20px;padding-bottom: 20px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;color: #AB6401;font-family: Georgia;font-size: 14px;line-height: 125%;text-align: left;"></td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                        <tr>
                                        	<td align="center" valign="top" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                            	<table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                    <tr>
                                                    	<td align="center" valign="top" style="border-top: 3px solid #363439;border-bottom: 3px solid #363439;padding-top: 20px;padding-bottom: 10px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                                        	<table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                            	<tr>
                                                                	<td align="center" colspan="2" valign="top" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                                                    	<table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                                        	<tr>
                                                                            	<td colspan="2" valign="top" class="bodyContent" style="padding-bottom: 20px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;color: #363439;font-family: Georgia;font-size: 16px;line-height: 175%;text-align: left;"><h4 style="display: block;font-family: Georgia;font-size: 14px;font-style: normal;font-weight: bold;line-height: 100%;letter-spacing: normal;margin-top: 0;margin-right: 0;margin-bottom: 10px;margin-left: 0;text-align: center;color: #AB6401 !important;">NEW FEATURES SINCE OUR LAUNCH</h4>
</td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            	<tr>
                                                                	<td valign="top" width="260" style="padding-right: 20px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                                            <tr>
                                                                                <td align="left" valign="mittle" width="77" style="padding-right: 13px;padding-bottom: 10px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;" mc:hideable="hideable_1" mchideable="hideable_1">
                                                                                    <img src="http://cdn-images.mailchimp.com/template_images/gallery/ee_colno_1.png" height="77" width="77" style="border: 0;height: auto;line-height: 100%;outline: none;text-decoration: none;">
                                                                                </td>
                                                                                <td valign="middle" width="" class="leftColumnContent" style="padding-bottom: 10px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;color: #434246;font-family: Georgia;font-size: 14px;line-height: 125%;text-align: left;"><br>
<strong>Grocery list</strong> organized into produce, meats, etc.</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td align="left" valign="middle" width="77" style="padding-top: 10px;padding-right: 13px;padding-bottom: 10px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;" mc:hideable="hideable_2" mchideable="hideable_2">
                                                                                    <img src="http://cdn-images.mailchimp.com/template_images/gallery/ee_colno_2.png" height="77" width="77" style="border: 0;height: auto;line-height: 100%;outline: none;text-decoration: none;">
                                                                                </td>
                                                                                <td valign="middle" width="" class="leftColumnContent" style="padding-top: 10px;padding-bottom: 10px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;color: #434246;font-family: Georgia;font-size: 14px;line-height: 125%;text-align: left;"><strong>Switch out</strong> any recipes you dislike in your plan</td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                    <td valign="top" width="260" style="padding-left: 20px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                                            <tr>
                                                                                <td align="left" valign="middle" width="77" style="padding-right: 13px;padding-bottom: 10px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;" mc:hideable="hideable_3" mchideable="hideable_3">
                                                                                    <img src="http://cdn-images.mailchimp.com/template_images/gallery/ee_colno_3.png" height="77" width="77" style="border: 0;height: auto;line-height: 100%;outline: none;text-decoration: none;">
                                                                                </td>
                                                                                <td valign="middle" width="" class="rightColumnContent" style="padding-top: 10px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;color: #434246;font-family: Georgia;font-size: 14px;line-height: 125%;text-align: left;"><strong>New plan&nbsp;</strong>emailed every Friday that matches your preferences</td>
                                                                            </tr>
                                                                            <tr>
                                                                                <td align="left" valign="middle" width="77" style="padding-top: 10px;padding-right: 13px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;" mc:hideable="hideable_4" mchideable="hideable_4">
                                                                                    <img src="http://cdn-images.mailchimp.com/template_images/gallery/ee_colno_4.png" height="77" width="77" style="border: 0;height: auto;line-height: 100%;outline: none;text-decoration: none;">
                                                                                </td>
                                                                                <td valign="middle" width="" class="rightColumnContent" style="padding-top: 10px;padding-bottom: 10px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;color: #434246;font-family: Georgia;font-size: 14px;line-height: 125%;text-align: left;"><strong>Expanded recipe collection- </strong>it&#39;s doubled!</td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                    	<td align="center" valign="top" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                                            <table border="0" cellpadding="0" cellspacing="0" width="100%">
                                                                <tr>
                                                                    <td valign="top" class="bodyContent" style="padding-top: 40px;padding-bottom: 10px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;color: #363439;font-family: Georgia;font-size: 16px;line-height: 175%;text-align: left;"><h2 style="display: block;font-family: Georgia;font-size: 20px;font-style: italic;font-weight: normal;line-height: 100%;letter-spacing: normal;margin-top: 0;margin-right: 0;margin-bottom: 10px;margin-left: 0;text-align: center;color: #AB6401 !important;">Ready to put dinner planning&nbsp;on autopilot?</h2>

<h3 style="display: block;font-family: Georgia;font-size: 16px;font-style: normal;font-weight: bold;line-height: 100%;letter-spacing: 1px;margin-top: 0;margin-right: 0;margin-bottom: 10px;margin-left: 0;text-align: center;color: #363439 !important;">Other users have already found it super helpful!</h3>
</td>
                                                                </tr>
                                                                <tr>
                                                                    <td align="center" valign="top" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                                                        <table border="0" cellpadding="15" cellspacing="0" class="templateButton" mc:hideable="hideable_5" mchideable="hideable_5" style="-moz-border-radius: 5px;-webkit-border-radius: 5px;background-color: #B16E12;border: 0;border-radius: 5px;">
                                                                            <tr>
                                                                                <td align="center" valign="middle" class="templateButtonContent" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;color: #FFFFFF;font-family: Georgia;font-size: 15px;font-weight: normal;letter-spacing: normal;line-height: 100%;text-align: center;text-decoration: none;"><a href="http://timesavorapp.com">Go to the Time Savor website</a></td>
                                                                            </tr>
                                                                        </table>
                                                                    </td>
                                                                </tr>
                                                                <tr>
                                                                    <td valign="top" class="bodyContent" style="padding-top: 40px;padding-bottom: 40px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;color: #363439;font-family: Georgia;font-size: 16px;line-height: 175%;text-align: left;"><h2 style="display: block;font-family: Georgia;font-size: 20px;font-style: italic;font-weight: normal;line-height: 100%;letter-spacing: normal;margin-top: 0;margin-right: 0;margin-bottom: 10px;margin-left: 0;text-align: center;color: #AB6401 !important;"><em>Sincerely,</em></h2>

<h3 style="display: block;font-family: Georgia;font-size: 16px;font-style: normal;font-weight: bold;line-height: 100%;letter-spacing: 1px;margin-top: 0;margin-right: 0;margin-bottom: 10px;margin-left: 0;text-align: center;color: #363439 !important;">Time Savor</h3>
</td>
                                                                </tr>
                                                            </table>
                                                        </td>
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                    <!-- END BODY \\ -->
                                </td>
                            </tr>
                        </table>
                        <!-- END CONTAINER \\ -->
                    </td>
                </tr>
                <tr>
                    <td align="center" valign="top" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                        <!-- // BEGIN FOOTER -->
                        <table border="0" cellpadding="0" cellspacing="0" width="100%">
                            <tr>
                                <td align="center" valign="top" style="padding-bottom: 40px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;">
                                    <table border="0" cellpadding="0" cellspacing="0" width="600" id="templateFooter">
                                        <tr>
                                            <td valign="top" class="footerContent" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;color: #FFFFFF;font-family: Georgia;font-size: 10px;line-height: 150%;text-align: center;">
                                                <em>Copyright &copy; *|CURRENT_YEAR|* *|LIST:COMPANY|*, All rights reserved.</em>
                                                <br>
                                                *|IFNOT:ARCHIVE_PAGE|* *|LIST:DESCRIPTION|*
                                                <br>
                                                <br>
                                                <strong>Our mailing address is:</strong>
                                                <br>
                                                *|HTML:LIST_ADDRESS_HTML|**|END:IF|* 
                                            </td>
                                        </tr>
                                        <tr>
                                            <td valign="top" class="footerContent" style="padding-top: 20px;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;color: #FFFFFF;font-family: Georgia;font-size: 10px;line-height: 150%;text-align: center;">
                                                <a href="*|UNSUB|*" style="color: #FFFFFF;font-weight: normal;text-decoration: underline;">unsubscribe from this list</a> | <a href="*|UPDATE_PROFILE|*" style="color: #FFFFFF;font-weight: normal;text-decoration: underline;">update subscription preferences</a>&nbsp;
                                                <br>
                                                <br>
                                                *|IF:REWARDS|* *|HTML:REWARDS|* *|END:IF|*
                                            </td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                        <!-- END FOOTER \\ -->
                    </td>
                </tr>
            </table>
        </center>
    </body>
</html>"""

def send_simple_message(email,html):
		return requests.post(
			"https://api.mailgun.net/v2/mg.timesavorapp.com/messages",
			auth=("api", "key-9y7c3fgcidcnqzopu-psjg0nq3wbg7h3"),
			data={"from": "Chef Sal <chefsal@mg.timesavorapp.com>",
				"to": email,
				"subject": "Hello, timesavor newsletter, check out what's new!",
				"html": html})


if __name__ == '__main__':
	from ts_server.models.account import *
	from ts_server.adapter.administration import connect_to_db

	connect_to_db("ts-server",'23.253.209.158',27017,'ts_server','a2e7rqej')
	email = []
	for acc in Account.objects:
		print "sending an email to %s"%acc.email
		email.append(acc.email)
	send_simple_message(email,html)

	



