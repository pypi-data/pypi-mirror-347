# coding: latin-1
# Copyright (C) 1986-2024 TQS Informatica Ltda
#
#  This software is provided 'as-is', without any express or implied
#  warranty. In no event will the authors be held liable for any damages
#  arising from the use of this software.
#
#  Permission is granted to anyone to use this software exclusively in
#  conjunction with TQS software, subject to the following restrictions:
#
#  1. The origin of this software must not be misrepresented. You must not
#     claim that you wrote the original software. If you use this software
#     in a product, an acknowledgment in the product documentation would be
#     required.
#  2. Altered source versions must be plainly marked as such, and must not be
#     misrepresented as being the original software.
#  3. This notice may not be removed or altered from any source distribution.
#
#  www.tqs.com.br
#  suporte@tqs.com.br
#-----------------------------------------------------------------------------
#    TQSEag.py         Acesso � API do EAG - Editor de Aplica��es Gr�ficas
#                      EAGW.EXE - M�dulo b�sico
#-----------------------------------------------------------------------------
import ctypes
import TQS.TQSUtil
import TQS.TQSJan

#-----------------------------------------------------------------------------
#    Constantes usadas em TQSEag.py
#    Rubberband
#
EAG_RUBNAO          = -1       # Sem rubberband        
EAG_RUBLINEAR       =  0       # Rubberband linear        
EAG_RUBRETANG       =  1       # Rubberband retangular    
EAG_RUBPANDIN       =  2       # Rubberband p/pan dinamico
#
#    Tipo de Rubberband
#
EAG_RUBRET_NAOPREEN = 0        # N�o preenche rubber retangular
EAG_RUBRET_JANW     = 1        # Preenche como janela W
EAG_RUBRET_JANC     = 2        # Preenche como janela C
EAG_RUBRET_JANUSR   = 3        # W (direita) ou C (esquerda)
#
#    Constantes de selecao de elementos
#
EAG_INORM           = 0        # Selecao normal        
EAG_IJANEL          = 1        # Selecao por janela entre 2 pts
EAG_ICURS           = 2        # Selecao na posicao do cursor    
EAG_IMULTP          = 4        # Selecao multipla
EAG_IALTJAN         = 8        # Primeiro cursor, depois janela
EAG_IJANELC         = 16       # Janela <C>
EAG_IJANELD         = 32       # Janela <D>

#-----------------------------------------------------------------------------
class Eag ():

    eagSingleton       = None                 # Objeto Singleton
    def __init__ (self):
        self.m_eagwexe = TQS.TQSUtil.LoadDll ("EAGW.EXE")
        self.m_eagvista= TQS.TQSUtil.LoadDll ("EAGVISTA.DLL")
        self.m_mdwg    = TQS.TQSUtil.LoadDll ("MDWG.DLL")
        self.entry     = Entry  (self)
        self.exec      = Exec   (self)
        self.msg       = Msg    (self)
        self.state     = State (self)
        self.locate    = Locate (self)
#
#    Objeto Singleton de acesso ao editor
#
    @classmethod
    def GetEag (self):
        """
        Retorna inst�ncia �nica Eag() do editor (Singleton).\n
        Use esta em vez de chamar Eag() toda vez e alocar recursos redundantes.
        """
        if             self.eagSingleton is None:
            self.eagSingleton = Eag ()
        return         self.eagSingleton
#
#    Retorna pedmv dado tqsjan
#
    def _GetPedmv (self, tqsjan):
            return     tqsjan.m_dwg.m_pedmv;

#-----------------------------------------------------------------------------
#    Pr�-entrada de dados do editor. 
#
class Entry ():
    ENTR_TECLA=0
    ENTR_COORD=1
    ENTR_STRIN=2

    def __init__ (self, eag):
        """
        Pr�-entrada de dados do editor EAG. \n
        Os comandos do EAG acionados a seguir consomem estas entradas.
        """
        self.m_eag     = eag

    def _Entrar (self, itipo, icod, x, y, str):
        paritipo       = ctypes.c_int (itipo)
        paricod        = ctypes.c_int (icod)
        parx           = ctypes.c_double (x)
        pary           = ctypes.c_double (y)
        parstr         = ctypes.c_char_p (str.encode(TQS.TQSUtil.CHARSET))
        self.m_eag.m_eagwexe.eag_FilaEntrada (paritipo, paricod, parx, pary, parstr)


    def KeyEscape (self):
        """
        Entra tecla de <Escape>
        """
        itipo          = Entry.ENTR_TECLA
        icod           = -1
        x              = 0.
        y              = 0.
        str            = ""
        self._Entrar   (itipo, icod, x, y, str)

    def KeyEnter (self):
        """
        Entra tecla de <Enter>
        """
        itipo          = Entry.ENTR_TECLA
        icod           = 0
        x              = 0.
        y              = 0.
        str            = ""
        self._Entrar   (itipo, icod, x, y, str)

    def KeyFunction (self, ishift, icontrol, ialt, ifn):
        """
        Entra tecla de fun��o Fn, opcionalmente com <Shift>, <Control> e <Alt> acionados
        """
        itipo          = Entry.ENTR_TECLA
        icod           = ifn + 20
        if             ifn >= 11:
            icod       = icod + 40 
        if             ishift != 0:
            icod       = icod + 10 
        if             icontrol  != 0:
            icod       = icod + 20 
        if             ialt   != 0:
            icod       = icod + 30 
        x              = 0.
        y              = 0.
        str            = ""
        self._Entrar   (itipo, icod, x, y, str)

    def String (self, str):
        """
        Entra um string, que ser� interpretado conforme o comando
        """
        itipo          = Entry.ENTR_STRIN
        icod           = 0
        x              = 0.
        y              = 0.
        self._Entrar   (itipo, icod, x, y, str)

    def Point (self, x, y):
        """
        Entra um par de coordenadas
        """
        itipo          = Entry.ENTR_COORD
        icod           = 1
        str            = ""
        self._Entrar   (itipo, icod, x, y, str)

#-----------------------------------------------------------------------------
#    Execu��o de comandos
#
class Exec ():

    def __init__ (self, eag):
        self.m_eag     = eag

    def Command (self, ident):
        """
        Executa um comando do editor.\n
        ident  : identificador tipo ID_xxx declarado no arquivo .MEN
        """
        parident       = ctypes.c_char_p (ident.encode(TQS.TQSUtil.CHARSET))
        self.m_eag.m_eagwexe.menu_acionamenu (parident)
        self.m_eag.m_eagwexe.eag_LimparEntrada ()

    def EnableCommand (self, ident, ienable):
        """
        Habilita ou desabilita um comando do editor. \n
        ident  : identificador tipo ID_xxx declarado no arquivo .MEN\n
        ienable: (0) desabilita (1) habilita comando
        """
        parident       = ctypes.c_char_p (ident.encode(TQS.TQSUtil.CHARSET))
        parienable     = ctypes.c_int (ienable)
        self.m_eag.m_eagwexe.menu_enable (parident, parienable)

    def CheckCommand (self, ident, icheck):
        """
        Coloca marca "Check" no comando, quando aplic�vel\n
        ident  : identificador tipo ID_xxx declarado no arquivo .MEN\n
        icheck : (0) n�o (1) marca check
        """
        parident       = ctypes.c_char_p (ident.encode(TQS.TQSUtil.CHARSET))
        paricheck      = ctypes.c_int (icheck)
        self.m_eag.m_eagwexe.menu_check (parident, paricheck)

    def EditW (self, name):
        """
        Chama o editor EDITW.EXE para edi��o de um arquivo Ascii fornecido\n
        name: Nome do arquivo, com ou sem path\n
        Retorna: (0) se editou (1) n�o
        """
        parname        = ctypes.c_char_p (name.encode(TQS.TQSUtil.CHARSET))
        istat          = 0
        paristat       = ctypes.c_int (istat)
        self.m_eag.m_eagwexe.eag_editw (parname, ctypes.byref (paristat))
        istat          = paristat.value
        return         istat


#-----------------------------------------------------------------------------
#    Mensagens na janela do editor
#
class Msg ():

    def __init__ (self, eag):
        self.m_eag     = eag

    def Print (self, *args):
        """
        Emite mensagens no estilo do "print" do Python, na janela do editor
        """
        txt                 = ""
        for                 msg in args:
            txt             += str (msg)
        par                 = ctypes.c_char_p (txt.encode(TQS.TQSUtil.CHARSET))
        self.m_eag.m_eagwexe.eag_msgs (par)

    def ClearMessageWindow (self):
        """
        Limpa a janela de mensagens do editor
        """
        self.m_eag.m_eagwexe.eag_msglimpa ()

    def PrintStatus (self, *args):
        """
        Emite mensagens no estilo do "print" do Python, na �rea de status do editor
        """
        txt                 = ""
        for                 msg in args:
            txt             += str (msg)
        par                 = ctypes.c_char_p (txt.encode(TQS.TQSUtil.CHARSET))
        self.m_eag.m_eagwexe.eag_statusmsg (par)

    def WindowTitle (self, tqsjan, title):
        """
        Define o t�tulo da janela atual de desenho\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        title:         Novo t�tulo da janela
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        partitle       = ctypes.c_char_p (title.encode(TQS.TQSUtil.CHARSET))
        self.m_eag.m_eagwexe.eag_titjan (parpvistav, partitle)

#-----------------------------------------------------------------------------
#    Localiza��o de elementos gr�ficos e leitura de coordenadas
#
class Locate ():

    def __init__ (self, eag):
        self.m_eag     = eag

    def GetPoint (self, tqsjan, msg):
        """
        L� um ponto do mouse/teclado.\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        msg:           Mensagem para leitura do ponto\n
        Retorna:       icod, x, y\n
        icod           (0)Enter (-1)Esc (1)Bot�o 1 (2)Bot�o 2 (3)Bot�o 3\n
                       (>20) Teclas de fun��o\n
                       (<-1) C�digo Ascii negativo ("A"=-65)
        """
        self.m_eag.msg.Print (msg)
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        icod           = 0
        x              = 0.
        y              = 0.
        paricod        = ctypes.c_int (icod)
        parx           = ctypes.c_double (x)
        pary           = ctypes.c_double (y)
        self.m_eag.m_eagwexe.eag_getpt (parpvistav, ctypes.byref (paricod),
                        ctypes.byref (parx), ctypes.byref (pary))
        icod           = paricod.value
        x              = parx.value
        y              = pary.value
        return         icod, x, y

    def GetSecondPoint (self, tqsjan, x1, y1, irubber, itprubret, msg):
        """
        L� um segundo ponto com mouse/teclado, fazendo rubberband com x1,y1\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        x1, y1         Ponto de refer�ncia para rubberband\n
        irubber:       Tipo de linha rubberband\n
                       TQSEag.EAG_RUBNAO           Sem rubberband        \n
                       TQSEag.EAG_RUBLINEAR        Rubberband linear        \n
                       TQSEag.EAG_RUBRETANG        Rubberband retangular    \n
                       TQSEag.EAG_RUBPANDIN        Rubberband p/pan dinamico\n
        itprubret:     Preenchimento de rubberband retangular\n
                       TQSEag.EAG_RUBRET_NAOPREEN  N�o preenche rubber ret\n
                       TQSEag.EAG_RUBRET_JANW      Preenche como janela W\n
                       TQSEag.EAG_RUBRET_JANC      Preenche como janela C\n
                       TQSEag.EAG_RUBRET_JANUSR    W (direita) ou C (esquerda)\n
        msg:           Mensagem para leitura do ponto\n
        Retorna:       icod, x, y\n
        icod           (0)Enter (-1)Esc (1)Bot�o 1 (2)Bot�o 2 (3)Bot�o 3\n
                       (>20) Teclas de fun��o\n
                       (<-1) C�digo Ascii negativo ("A"=-65)
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        parx1          = ctypes.c_double (x1)
        pary1          = ctypes.c_double (y1)
        parirubbet     = ctypes.c_int (irubber)
        paritprubret   = ctypes.c_int (itprubret)
        parmsg         = ctypes.c_char_p (msg.encode(TQS.TQSUtil.CHARSET))
        icod           = 0
        x2             = 0.
        y2             = 0.
        paricod        = ctypes.c_int (icod)
        parx2          = ctypes.c_double (x2)
        pary2          = ctypes.c_double (y2)
        self.m_eag.m_eagwexe.eag_get1px (parpvistav, ctypes.byref (paricod),
                       parx1, pary1, ctypes.byref (parx2), ctypes.byref (pary2),
                       parirubbet, paritprubret, parmsg)
        icod           = paricod.value
        x2             = parx2.value
        y2             = pary2.value
        return         icod, x2, y2

    def SetNextZ (self, z):
        """
        Define coordenadas Z que podem ser usadas pelo pr�ximo comando\n
        A coordenada � zerada ap�s o pr�ximo GetPoint
        """
        parz           = ctypes.c_double (z)
        self.m_eag.m_eagwexe.eag_get1p_defz (parz)

    def GetLastZ (self):
        """
        Retorna (idisp, z) o valor da cota Z da �ltima entrada, se dispon�vel\n
        idisp:         (1) Se cota Z dizpon�vel\n
        z              Valor, se dispon�vel
        """
        idisp          = 0
        paridisp       = ctypes.c_int (idisp)
        z              = 0.
        parz           = ctypes.c_double (z)
        self.m_eag.m_eagwexe.eag_zinput (ctypes.byref (paridisp), ctypes.byref (parz))
        idisp          = paridisp.value
        z              = parz.value
        return         idisp, z

    def GetLabel (self, tqsjan, msg):
        """
        L� texto do usu�rio, com mensagem\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        msg:           Mensagem\n
        Retorna:       str, istat\n
        str:           Texto lido\n
        istat          (0) Ok (1) Enter (2) Esc
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        parmsg         = ctypes.c_char_p (msg.encode(TQS.TQSUtil.CHARSET))
        parstr         = ctypes.create_string_buffer (TQS.TQSUtil.MAXNCSTR)
        istat          = 0
        paristat       = ctypes.c_int (istat)
        self.m_eag.m_eagwexe.eag_peglab (parpvistav, parmsg, parstr, ctypes.byref (paristat))
        str            = parstr.value.decode(TQS.TQSUtil.CHARSET)
        istat          = paristat.value
        return         str, istat

    def GetValue (self, tqsjan, msg, valmin, valmax, valdef):
        """
        Leitura de n�mero em ponto flutuante.\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        msg:           Mensagem\n
        valmin:        Valor m�nimo\n
        valmax:        Valor m�ximo\n
        valdef:        Valor default\n
        Retorna:       val, istat\n
        val:           Valor lido\n
        istat:         (0) Ok (1) N�o leu
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        parmsg         = ctypes.c_char_p (msg.encode(TQS.TQSUtil.CHARSET))
        parvalmin      = ctypes.c_double (valmin)
        parvalmax      = ctypes.c_double (valmax)
        parvaldef      = ctypes.c_double (valdef)
        dadunid        = 0
        pardadunid     = ctypes.c_void_p (dadunid)
        val            = 0.
        parval         = ctypes.c_double (val)
        istat          = 0
        paristat       = ctypes.c_int (istat)
        self.m_eag.m_eagwexe.eag_grream (parpvistav, parmsg, ctypes.byref (parval),
                         parvalmin, parvalmax, parvaldef, pardadunid, 
                         ctypes.byref (paristat))
        val            = parval.value
        istat          = paristat.value
        return         val, istat

    def GetAngle (self, tqsjan, msg, angdef):
        """
        Leitura de um �ngulo em graus. Aceita entrada de <R> 3 pontos e <L> linha\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        msg:           Mensagem\n
        angdef:        Valor default\n
        Retorna:       val, istat\n
        ang:           �ngulo lido\n
        istat:         (0) Ok (1) N�o leu
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        parmsg         = ctypes.c_char_p (msg.encode(TQS.TQSUtil.CHARSET))
        parangdef      = ctypes.c_double (angdef)
        ang            = 0.
        istat          = 0
        parang         = ctypes.c_double (ang)
        paristat       = ctypes.c_int (istat)
        self.m_eag.m_eagwexe.eag_girang (parpvistav, parmsg, ctypes.byref (parang),
                       parangdef, ctypes.byref (paristat))
        ang            = parang.value
        istat          = paristat.value
        return         ang, istat

    def GetEntryType (self):
        """
        Retorna (0) para �ltima entrada alfanum�rica ou (1) gr�fica
        """
        istat          = 0
        paristat       = ctypes.c_int (istat)
        self.m_eag.m_eagwexe.eag_gregra (ctypes.byref (paristat))
        istat          = paristat.value
        return         istat

    def GetYesNo (self, tqsjan, msg, r1, r2):
        """
        Mostrar mensagem msg e retorna resposta tipo sim (r1) ou n�o (r2)\n
        Retorna:\n
        istat:         (0) r1 (1) r2 (2) <Escape>\n
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        parmsg         = ctypes.c_char_p (msg.encode(TQS.TQSUtil.CHARSET))
        parr1          = ctypes.c_char_p (r1.encode(TQS.TQSUtil.CHARSET))
        parr2          = ctypes.c_char_p (r2.encode(TQS.TQSUtil.CHARSET))
        istat          = 0
        paristat       = ctypes.c_int (istat)
        self.m_eag.m_eagwexe.eag_pegsix (parpvistav, parmsg, parr1, parr2,
                       ctypes.byref (paristat))
        istat          = paristat.value
        return         istat

    def GetCursor (self, tqsjan):
        """
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        Retorna coordenadas x,y da posi��o do cursor no mundo real\n
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        x              = 0.
        y              = 0.
        parx           = ctypes.c_double (x)
        pary           = ctypes.c_double (y)
        self.m_eag.m_eagwexe.eag_lercursor (parpvistav, ctypes.byref (parx), 
                        ctypes.byref (pary))
        x              = parx.value
        y              = pary.value
        return         x, y
    
    def SetRubberIdle (self, tqsjan, irubberidle, xrubbidle, yrubbidle):
        """
        Liga linha el�stica com ponto de refer�ncia fornecido.\n
        A linha fica acesa at� o pr�ximo comando ou <Escape>\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        parirubberidle = ctypes.c_int (irubberidle)
        parxrubbidle   = ctypes.c_double (xrubbidle)
        paryrubbidle   = ctypes.c_double (yrubbidle)
        self.m_eag.m_eagwexe.eag_rubberidle (parpvistav, parirubberidle, 
                       parxrubbidle, paryrubbidle)

    def GetPolyline (self, tqsjan):
        """
        L� poligonal\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        Retorna:\n
        xy[][2]        Matriz de pontos lidos. N�o leu se == 0
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        self.m_eag.m_eagwexe.eag_getplnAcum (parpvistav)
        npt            = 0
        parnpt         = ctypes.c_int (npt)
        self.m_eag.m_eagwexe.eag_getplnAcumNpt (ctypes.byref (parnpt))
        npt            = parnpt.value
        xy             = []
        if             npt < 3:
            return     xy
        for            ipt in range (0, npt):
            paript     = ctypes.c_int (ipt)
            x          = 0.
            parx       = ctypes.c_double (x)
            y          = 0.
            pary       = ctypes.c_double (y)
            self.m_eag.m_eagwexe.eag_getplnAcumLerPt (paript, ctypes.byref (parx), ctypes.byref (pary))
            xy.append  ([parx.value, pary.value])

        return         xy

    def Select (self, tqsjan, msg, itploc):
        """
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        Faz sele��o de elementos conforme itploc. Emite mensagem do usu�rio.\n
        Retorna 1o elemento da sele��o. Para mais elementos, use BeginSelect/GetSelect\n
        msg:           Mensagem ao usu�rio\n
        itploc:        Tipo de sele��o:\n
                        TQSEag.EAG_INORM   Normal\n
                        TQSEag.EAG_IJANEL  Sele��o por janela\n
                        TQSEag.EAG_ICURS   Coordenada do cursor\n
                        TQSEag.EAG_IMULTP  Sele��o m�ltipla\n
                        TQSEag.EAG_IALTJAN Tenta ponto, depois janela\n
        Retorna:\n
        addr:           Handle do 1o elemento gr�fico selecionado (DWG)\n
        x:              Coordenadas de sele��o\n
        y:              Coordenadas de sele��o\n
        np:             �ndice do ponto se poligonal\n
        istat:          (!=0) Se n�o selecionou
        """
        self.m_eag.msg.Print (msg)
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        parmsg         = ctypes.c_char_p (msg.encode(TQS.TQSUtil.CHARSET))
        paritploc      = ctypes.c_int (itploc)
        iadr           = 0
        pariadr        = ctypes.c_void_p (iadr)
        x              = 0.
        y              = 0.
        np             = 0
        istat          = 0
        parx           = ctypes.c_double (x)
        pary           = ctypes.c_double (y)
        parnp          = ctypes.c_int (np)
        paristat       = ctypes.c_int (istat)
        self.m_eag.m_eagwexe.eag_locelm (parpvistav, ctypes.byref (pariadr),
                       ctypes.byref (parx), ctypes.byref (pary), 
                       ctypes.byref (parnp), parmsg, paritploc, ctypes.byref (paristat))
        iadr          = pariadr.value
        x              = parx.value
        y              = pary.value
        np             = parnp.value
        istat          = paristat.value
        return         iadr, x, y, np, istat


    def BeginSelection (self, tqsjan):
        """
        Prepara para a leitura de elementos selecionados em Select\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        Retorna (1) se n�o h� elementos
        """
        pedmv          = self.m_eag._GetPedmv (tqsjan)
        parpedmv       = ctypes.c_void_p (pedmv)
        nwst           = 0
        parnwst        = ctypes.c_int (nwst)
        self.m_eag.m_mdwg.g_wstnum (parpedmv, ctypes.byref (parnwst))
        nwst           = parnwst.value
        if             nwst == 0:
            return     1
        self.m_eag.m_mdwg.g_wstrew (parpedmv)
        return         0

    def NextSelection (self, tqsjan):
        """
        Retorna handle para o pr�ximo elemento gr�fico selecionado ou None\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG
        """

        addr           = 0
        pedmv          = self.m_eag._GetPedmv (tqsjan)
        parpedmv       = ctypes.c_void_p (pedmv)
        paradr         = ctypes.c_void_p (addr)
        istat          = 0
        paristat       = ctypes.c_int (istat)
        self.m_eag.m_mdwg.g_wstler (parpedmv, ctypes.byref (paradr), ctypes.byref (paristat))
        addr           = paradr.value
        istat          = paristat.value
        if             istat != 0:
            return     None
        return         addr

    def DragSelection (self, tqsjan, xref, yref):
        """
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        Acende elementos os selecionados e os arrasta junto com o cursor\n
        xref,yref � o ponto de inser��o inicial da lista
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        parxref        = ctypes.c_double (xref)
        paryref        = ctypes.c_double (yref)
        self.m_eag.m_eagwexe.eag_dragws (parpvistav, parxref, paryref)

    def DragOff (self, tqsjan):
        """
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        Desliga elementos ligados em DragSelection
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        self.m_eag.m_eagwexe.eag_desligressaltowst (parpvistav)


#-----------------------------------------------------------------------------
#    Controle de vari�veis de estado do editor
#
class State ():

    def __init__ (self, eag):
        self.m_eag     = eag

    def GetOrtho (self, tqsjan):
        """
        Modo ortogonal\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        Retorna:\n
        iortho:        (0) desligado (1) modo ortogonal\n
        angle:         �ngulo em graus do modo ortogonal
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        iorto          = 0
        pariorto       = ctypes.c_int (iorto)
        angle          = 0
        parangle       = ctypes.c_double (angle)
        self.m_eag.m_eagwexe.eag_ortoler (parpvistav, ctypes.byref (pariorto), 
                         ctypes.byref (parangle))
        iorto          = pariorto.value
        angle          = parangle.value
        return         iorto, angle

    def SetOrtho (self, tqsjan, iortho, angle):
        """
        Modo ortogonal\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        iortho:        (0) Desligado (1) Modo ortogonal\n
        angle:         �ngulo em graus do modo ortogonal
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        pariorto       = ctypes.c_int (iortho)
        parangle       = ctypes.c_double (angle)
        self.m_eag.m_eagwexe.eag_ortogrv (parpvistav, pariorto, parangle)

    def GetLevelLock (self, tqsjan):
        """
        N�vel travado\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        Retorna:\n
        ilevellock:    (0) Desligado (1) N�vel travado
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        ilevellock     = 0
        parilevellock  = ctypes.c_int (ilevellock)
        self.m_eag.m_eagwexe.eag_levllk (parpvistav, ctypes.byref (parilevellock))
        ilevellock     = parilevellock.value
        return         ilevellock

    def SetLevelLock (self, tqsjan, ilevellock):
        """
        N�vel travado\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        ilevellock:    (0) Desligado (1) N�vel travado
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        parilevellock  = ctypes.c_int (ilevellock)
        self.m_eag.m_eagwexe.eag_grvllk (parpvistav, parilevellock)

    def ClearAllLevelsLock (self, tqsjan):
        """
        Limpa travas individuais de n�veis\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        self.m_eag.m_eagwexe.eag_limpatrava (parpvistav)

    def GetOneLevelLock (self, tqsjan, ilevel):
        """
        L� a trava de um n�vel\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        ilevel:        N�vel considerado\n
        Retorna:\n
        ilock:         (1) Se este n�vel est� travado
        """
        pedmv          = self.m_eag._GetPedmv (tqsjan)
        parpedmv       = ctypes.c_void_p (pedmv)
        parilevel      = ctypes.c_int (ilevel)
        ilock          = 0
        parilock       = ctypes.c_int (ilock)
        self.m_eag.m_mdwg.g_lertravanivel (parpedmv, parilevel, ctypes.byref (parilock))
        ilock          = parilock.value
        return         ilock

    def SetOneLevelLock (self, tqsjan, ilevel, ilock):
        """
        Define a trava de um n�vel\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        ilevel:        N�vel considerado\n
        ilock:         (1) Se este n�vel est� travado
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        parilevel      = ctypes.c_int (ilevel)
        parilock       = ctypes.c_int (ilock)
        self.m_eag.m_eagwexe.eag_definetrava (parpvistav, parilevel, parilock)

    def GetActiveLevel (self, tqsjan):
        """
        Define o n�vel atual\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        Retorna:\n
        iactivelevel:   (0) Desligado (1) N�vel travado
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        iactivelevel   = 0
        pariactivelevel= ctypes.c_int (iactivelevel)
        self.m_eag.m_eagwexe.eag_iatnivler (parpvistav, ctypes.byref (pariactivelevel))
        iactivelevel   = pariactivelevel.value
        return         iactivelevel

    def SetActiveLevel (self, tqsjan, iactivelevel):
        """
        N�vel atual\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        iactivelevel:  N�vel atual - dos elementos a serem criados.
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        pariactivelevel= ctypes.c_int (iactivelevel)
        self.m_eag.m_eagwexe.eag_iatnivgrv (parpvistav, pariactivelevel)

    def GetFastCurve (self, tqsjan):
        """
        Retorna (1) se curva r�pida ligada\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        Retorna:\n
        ifastcurve:    (0) modo normal (1) curva r�pida (curvas mostradas como linhas)
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        ifastcurve     = 0
        parifastcurve  = ctypes.c_int (ifastcurve)
        self.m_eag.m_eagvista.vis_lericurvar (parpvistav, ctypes.byref (parifastcurve))
        ifastcurve    = parifastcurve.value
        return         ifastcurve

    def SetFastCurve (self, tqsjan, ifastcurve):
        """
        Define (1) se curva r�pida ligada\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        ifastcurve:    (0) modo normal (1) curva r�pida (curvas mostradas como linhas)
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        parifastcurve  = ctypes.c_int (ifastcurve)
        self.m_eag.m_eagvista.vis_grvicurvar (parpvistav, parifastcurve)
        ifastcurve    = parifastcurve.value

    def GetGrid (self, tqsjan):
        """
        Retorna dados de grade\n
        tqsjan         objeto da classe TQS.TQSJan.Window passado pelo EAG\n
	Retorna:\n
        igrade:        (0) N�o (1) Grade ligada\n
        grdorx:        X origem da grade cm\n
        grdory:        Y origem da grade cm\n
        grdesx:        X espa�amento da grade cm\n
        grdesy:        Y espa�amento da grade cm\n
        grdang:        �ngulo da grade, em graus\n
        iespacponto:   N�mero de espa�amentos por ponto da grade\n
        igraderubber:  (1) Se grade em linha el�stica
        """
        pedmv          = self.m_eag._GetPedmv (tqsjan)
        parpedmv     = ctypes.c_void_p (pedmv)
        igrade        = 0
        parigrade    = ctypes.c_int (igrade)
        grdorx        = 0.
        pargrdorx    = ctypes.c_double (grdorx)
        grdory        = 0.
        pargrdory    = ctypes.c_double (grdory)
        grdesx        = 0.
        pargrdesx    = ctypes.c_double (grdesx)
        grdesy        = 0.
        pargrdesy    = ctypes.c_double (grdesy)
        grdang        = 0.
        pargrdang    = ctypes.c_double (grdang)
        iespacponto    = 0
        pariespacponto    = ctypes.c_int (iespacponto)
        igraderubber    = 0
        parigraderubber    = ctypes.c_int (igraderubber)
        self.m_eag.m_mdwg.g_exlerigrade (parpedmv, ctypes.byref (parigrade),
            ctypes.byref (pargrdorx), ctypes.byref (pargrdory),
            ctypes.byref (pargrdesx), ctypes.byref (pargrdesy),
            ctypes.byref (pargrdang), ctypes.byref (pariespacponto),
            ctypes.byref (parigraderubber))
        igrade        = parigrade.value
        grdorx        = pargrdorx.value
        grdory        = pargrdory.value
        grdesx        = pargrdesx.value
        grdesy        = pargrdesy.value
        grdang        = pargrdang.value
        iespacponto    = pariespacponto.value
        igraderubber    = parigraderubber.value
        return        igrade, grdorx, grdory, grdesx, grdesy, grdang, iespacponto, igraderubber

    def SetGrid (self, tqsjan, igrade, grdorx, grdory, grdesx, grdesy, grdang, 
                 iespacponto, igraderubber):
        """
        Define dados da grade\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        igrade:        (0) N�o (1) Grade ligada\n
        grdorx:        X origem da grade cm\n
        grdory:        Y origem da grade cm\n
        grdesx:        X espa�amento da grade cm\n
        grdesy:        Y espa�amento da grade cm\n
        grdang:        �ngulo da grade, em graus\n
        iespacponto:   N�mero de espa�amentos por ponto da grade\n
        igraderubber:  (1) Se grade em rubberband
        """
        pedmv          = self.m_eag._GetPedmv (tqsjan)
        parpedmv     = ctypes.c_void_p (pedmv)
        parigrade    = ctypes.c_int (igrade)
        pargrdorx    = ctypes.c_double (grdorx)
        pargrdory    = ctypes.c_double (grdory)
        pargrdesx    = ctypes.c_double (grdesx)
        pargrdesy    = ctypes.c_double (grdesy)
        pargrdang    = ctypes.c_double (grdang)
        pariespacponto    = ctypes.c_int (iespacponto)
        parigraderubber    = ctypes.c_int (igraderubber)
        self.m_eag.m_mdwg.g_exgrvigrade (parpedmv, parigrade,
            pargrdorx, pargrdory, pargrdesx, pargrdesy, pargrdang, pariespacponto,
            parigraderubber)

    def InvertCapture (self, tqsjan):
        """
        Inverte a captura de coordenadas (ligada ou desligada)\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        self.m_eag.m_eagwexe.eag_capinv (parpvistav)

    def GetFatText (self, tqsjan):
        """
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        Retorna o modo de texto r�pido\n
        ifast:         (1) se modo de texto r�pido
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        ifast          = 0
        parifast       = ctypes.c_int (ifast)
        self.m_eag.m_eagvista.vis_leritextor (parpvistav, ctypes.byref (parifast))
        ifast          = parifast.value
        return         ifast

    def SetFatText  (self, tqsjan, ifast):
        """
        Define o modo de texto r�pido\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        ifast:         (1) se modo de texto r�pido
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        parifast       = ctypes.c_int (ifast)
        self.m_eag.m_eagvista.vis_grvitextor (parpvistav, parifast)

    def GetBlockInsertion (self, tqsjan):
        """
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        Retorna dados para inser��o de um bloco novo:\n
        xscale:        Escala X\n
        yscale:        Escala Y\n
        angle:         �ngulo de inser��o em graus
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        xscale         = 0.
        yscale         = 0.
        angle          = 0.
        parxscale      = ctypes.c_double (xscale)
        paryscale      = ctypes.c_double (yscale)
        parangle       = ctypes.c_double (angle)
        self.m_eag.m_eagwexe.eag_iatbloler (parpvistav, ctypes.byref (parxscale),
                        ctypes.byref (paryscale), ctypes.byref (parangle))
        xscale         = parxscale.value
        yscale         = paryscale.value
        angle          = parangle.value
        return         xscale, yscale, angle

    def SetBlockInsertion (self, tqsjan, xscale, yscale, angle):
        """
        Define dados para inser��o de um bloco novo:\n
        tqsjan:       objeto da classe TQS.TQSJan.Window passado pelo EAG\n
        xscale:       Escala X\n
        yscale:       Escala Y\n
        angle:        �ngulo de inser��o em graus
        """
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        parxscale      = ctypes.c_double (xscale)
        paryscale      = ctypes.c_double (yscale)
        parangle       = ctypes.c_double (angle)
        self.m_eag.m_eagwexe.eag_iatblogrv (parpvistav, parxscale, paryscale, parangle)

    def _PegarDistArr (self, tqsjan):
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        atoffs         = 0.
        paratoffs      = ctypes.c_double (atoffs)
        atrfil         = 0.
        paratrfil      = ctypes.c_double (atrfil)
        atcrd1         = 0.
        paratcrd1      = ctypes.c_double (atcrd1)
        atcrd2         = 0.
        paratcrd2      = ctypes.c_double (atcrd2)
        self.m_eag.m_eagwexe.eag_iatoffler (parpvistav, ctypes.byref (paratoffs), 
                       ctypes.byref (paratrfil), ctypes.byref (paratcrd1), 
                       ctypes.byref (paratcrd2))
        atoffs         = paratoffs.value
        atrfil         = paratrfil.value
        atcrd1         = paratcrd1.value
        atcrd2         = paratcrd2.value
        return        atoffs, atrfil, atcrd1, atcrd2

    def _DefDistArr (self, tqsjan, atoffs, atrfil, atcrd1, atcrd2):
        parpvistav     = ctypes.c_void_p (tqsjan.m_pvistav)
        paratoffs      = ctypes.c_double (atoffs)
        paratrfil      = ctypes.c_double (atrfil)
        paratcrd1      = ctypes.c_double (atcrd1)
        paratcrd2      = ctypes.c_double (atcrd2)
        self.m_eag.m_eagwexe.eag_iatoffgrv (parpvistav, paratoffs, paratrfil,
                        paratcrd1, paratcrd2)

    def GetParallelDist (self, tqsjan):
        """
        Retorna dist�ncia padr�o no comando "Paralela a elemento"
        """
        atoffs, atrfil, atcrd1, atcrd2 = self._PegarDistArr (tqsjan)
        return         atoffs

    def SetParallelDist (self, tqsjan, distance):
        """
        Define dist�ncia padr�o no comando "Paralela a elemento"
        """
        atoffs, atrfil, atcrd1, atcrd2 = self._PegarDistArr (tqsjan)
        self._DefDistArr (tqsjan, distance, atrfil, atcrd1, atcrd2)

    def GetFilletRadius (self, tqsjan):
        """
        Retorna a dist�ncia de arredondamento padr�o de arcos
        """
        atoffs, atrfil, atcrd1, atcrd2 = self._PegarDistArr (tqsjan)
        return         atrfil

    def SetFilletRadius (self, tqsjan, radius):
        """
        Define a dist�ncia de arredondamento padr�o de arcos
        """
        atoffs, atrfil, atcrd1, atcrd2 = self._PegarDistArr (tqsjan)
        self._DefDistArr (tqsjan, atoffs, radius, atcrd1, atcrd2)

    def GetFilletlDist (self, tqsjan):
        """
        Retorna dist�ncias padr�o de chanfragem:
        dist1, dist2:  Dist�ncias de chanfragem
        """
        atoffs, atrfil, atcrd1, atcrd2 = self._PegarDistArr (tqsjan)
        return         atcrd1, atcrd2

    def SetFilletlDist (self, tqsjan, dist1, dist2):
        """
        Define dist�ncias padr�o de chanfragem
        dist1, dist2:  Dist�ncias de chanfragem
        """
        atoffs, atrfil, atcrd1, atcrd2 = self._PegarDistArr (tqsjan)
        self._DefDistArr (tqsjan, atoffs, atrfil, dist1, dist2)


