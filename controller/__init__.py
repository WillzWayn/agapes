#!/usr/bin/python
# -*- encoding: utf-8 -*-
"""
PSG - Tecnologia Aplicada

Este é um módulo utilizado para contagem de falhas em
plantações de cana-de-açúcar através do uso de imagens
aéreas capturadas por VANT's ou aparelhos similares.

Este arquivo é responsável pelo desenho da interface do
programa e também pela execução e apresentação dos
resultados obtidos com a imagem fornecida.
"""
from multiprocessing import Queue, Pipe
from gui.event import PostEvent
import threading
import core

__all__ = [
    "Execute",
    "LoadImage",
    "SegmentImage",
    "ProcessImage",
]

def Execute(*args):
    """
    Executa o algoritmo com os dados parâmetros. Eventos são
    disparados e podem ter tratamentos diferenciados dependendo
    do modo em que o programa está sendo executado: através de
    uma GUI ou a partir da linha de comando.
    :param args Argumentos passados à função.
    """
    if None in args:
        from .ui import ControlUI
        ControlUI()

    else:
        from .cmd import ControlCommandLine
        ControlCommandLine(*args)

def ThreadWrapper(function):
    """
    Invólucro de funções a serem executadas em um thread.
    :param function Função a ser envolvida.
    """
    def threadf(*args, **kwargs):
        t = threading.Thread(target = function, args = args, kwargs = kwargs)
        t.start()

    return threadf

def LoadImage(address, context = None):
    """
    Carrega uma imagem.
    :param address Endereço da imagem a ser carregada.
    :return core.Image Imagem carregada.
    """
    img = core.LoadImage(address)
    PostEvent("ImageLoaded", img, context = context)

    return img

def SegmentImage(img, context = None):
    """
    Executa a segmentação da imagem.
    :param img Imagem a ser segmentada.
    :return Image, ComponentList, Map Lista de componentes.
    """
    img, comp, cmap = core.SegmentImage(img)
    PostEvent("ImageSegmented", img, context = context)

    return img, comp, cmap

def ProcessImage(cmap, distance, context = None):
    """
    Processa a imagem e procura por linhas de plantação
    de cana-de-açúcar; e desenha sobre a imagem as linhas
    encontradas.
    :param cmap Mapa de componentes da imagem.
    :param distance Distância entre linhas da plantação.
    :return Image, float, float Porcentagem e metragem de falhas.
    """
    img, lines, pcent, meter = core.ProcessImage(cmap, distance)
    PostEvent("ImageProcessed", img, pcent, meter, context = context)

    return img, lines, pcent, meter

