# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 3.10.1-0-g8feb16b3)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
from .link_toggle import LinkToggle

###########################################################################
## Class ConfigDialogBase
###########################################################################

class ConfigDialogBase ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Transform It", pos = wx.DefaultPosition, size = wx.DefaultSize, style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

		bSizer1 = wx.BoxSizer( wx.VERTICAL )

		self.m_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer3 = wx.BoxSizer( wx.VERTICAL )

		fgSizer1 = wx.FlexGridSizer( 0, 3, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

		self.m_staticText1 = wx.StaticText( self.m_panel, wx.ID_ANY, u"Horizontal (%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText1.Wrap( -1 )

		fgSizer1.Add( self.m_staticText1, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_horizontalScale = wx.SpinCtrlDouble( self.m_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 10000, 100, 5 )
		self.m_horizontalScale.SetDigits( 2 )
		fgSizer1.Add( self.m_horizontalScale, 0, wx.EXPAND|wx.ALL, 5 )

		self.m_horizontalMirror = wx.CheckBox( self.m_panel, wx.ID_ANY, u"Mirror", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.m_horizontalMirror, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


		fgSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_linkButton = LinkToggle(self.m_panel)
		self.m_linkButton.SetToolTip( u"Preserve aspect ratio" )
		self.m_linkButton.SetMinSize( wx.Size( 28,16 ) )

		fgSizer1.Add( self.m_linkButton, 0, wx.ALIGN_CENTER_HORIZONTAL, 5 )


		fgSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText2 = wx.StaticText( self.m_panel, wx.ID_ANY, u"Vertical (%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText2.Wrap( -1 )

		fgSizer1.Add( self.m_staticText2, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_verticalScale = wx.SpinCtrlDouble( self.m_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 10000, 100, 5 )
		self.m_verticalScale.SetDigits( 2 )
		self.m_verticalScale.Enable( False )

		fgSizer1.Add( self.m_verticalScale, 0, wx.EXPAND|wx.ALL, 5 )

		self.m_verticalMirror = wx.CheckBox( self.m_panel, wx.ID_ANY, u"Mirror", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_verticalMirror.Enable( False )

		fgSizer1.Add( self.m_verticalMirror, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_staticText3 = wx.StaticText( self.m_panel, wx.ID_ANY, u"Rotation (deg)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText3.Wrap( -1 )

		fgSizer1.Add( self.m_staticText3, 0, wx.ALL, 5 )

		self.m_rotation = wx.SpinCtrlDouble( self.m_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, -360, 360, 0, 5 )
		self.m_rotation.SetDigits( 2 )
		fgSizer1.Add( self.m_rotation, 0, wx.ALL|wx.EXPAND, 5 )

		self.m_staticText4 = wx.StaticText( self.m_panel, wx.ID_ANY, u"(positive - cw)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )

		fgSizer1.Add( self.m_staticText4, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

		self.m_staticText5 = wx.StaticText( self.m_panel, wx.ID_ANY, u"Shape width (%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText5.Wrap( -1 )

		fgSizer1.Add( self.m_staticText5, 0, wx.ALL, 5 )

		self.m_shapeWidth = wx.SpinCtrlDouble( self.m_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 10000, 100, 5 )
		self.m_shapeWidth.SetDigits( 2 )
		fgSizer1.Add( self.m_shapeWidth, 0, wx.ALL, 5 )


		fgSizer1.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_staticText6 = wx.StaticText( self.m_panel, wx.ID_ANY, u"Track width (%)", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText6.Wrap( -1 )

		fgSizer1.Add( self.m_staticText6, 0, wx.ALL, 5 )

		self.m_trackWidth = wx.SpinCtrlDouble( self.m_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 10000, 100, 5 )
		self.m_trackWidth.SetDigits( 2 )
		fgSizer1.Add( self.m_trackWidth, 0, wx.ALL, 5 )


		bSizer3.Add( fgSizer1, 1, wx.EXPAND, 5 )

		self.m_staticline1 = wx.StaticLine( self.m_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer3.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

		m_sdbSizer1 = wx.StdDialogButtonSizer()
		self.m_sdbSizer1OK = wx.Button( self.m_panel, wx.ID_OK )
		m_sdbSizer1.AddButton( self.m_sdbSizer1OK )
		self.m_sdbSizer1Cancel = wx.Button( self.m_panel, wx.ID_CANCEL )
		m_sdbSizer1.AddButton( self.m_sdbSizer1Cancel )
		m_sdbSizer1.Realize();

		bSizer3.Add( m_sdbSizer1, 0, wx.BOTTOM|wx.EXPAND, 5 )


		self.m_panel.SetSizer( bSizer3 )
		self.m_panel.Layout()
		bSizer3.Fit( self.m_panel )
		bSizer1.Add( self.m_panel, 1, wx.EXPAND, 5 )


		self.SetSizer( bSizer1 )
		self.Layout()
		bSizer1.Fit( self )

		self.Centre( wx.BOTH )

	def __del__( self ):
		pass


