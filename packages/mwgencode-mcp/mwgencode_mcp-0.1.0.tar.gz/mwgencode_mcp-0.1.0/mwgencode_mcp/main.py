from mcp.server.fastmcp import FastMCP
from typing import TextIO
import logging
from gencode.gen_code import GenCode,GenProject_Sample,GenProject_Flask,GenProject_Aiohttp,GenSwagger
from gencode.importmdj.import_swagger2_class import  ImportSwagger
import argparse
import os
import sys
from gencode.gencode.export_class2swgclass import ExportClass2SWGClass
import yaml
import gencode.upgrade as upgrade


os.environ["FASTMCP_PORT"] = "8300"

mcp = FastMCP("mwgencode 🚀", init_timeout=30, init_retry=3)

class Gen_Code():
    def __init__(self,args):
        self.args = args
        self.prj_conf = None

    def _get_config(self) -> dict:
        def load_config():
            cnfgfile = os.path.join(os.path.abspath(self.args.get('root_path','.')), 'gen_code.yaml')
            if not os.path.exists(cnfgfile):
                raise Exception('gen_code.yaml文件不存在，请先执行 gencode init 初始化项目！')
            yml = open(cnfgfile)
            try:
                self.prj_conf = yaml.full_load(yml)
            except Exception as e:
                raise Exception('载入 gen_code.yaml 出错，error:%s' % e)
            return self.prj_conf
        if self.prj_conf is None:
            self.prj_conf  = load_config()
        return self.prj_conf

    def _get_apptype(self):
        try:
            return self._get_config().get('project', {}).get('type', 'flask')
        except Exception as e:
            raise Exception('gen_code.yaml 文件内容出错，%s' % e)

    def _get_rootpath(self):
        try:
            # cmd有指定rootpath 时，以指定的rootpath
            return self.args.get('root_path') if self.args.get('root_path','.')!='.' else self._get_config().get('project',{}).get('rootpath','.')
        except Exception as e:
            raise Exception('gen_code.yaml 文件内容出错，%s'%e)

    def _get_umlfile(self):
        try:
            return os.path.join(self._get_rootpath(),
                                   self._get_config()['project']['doc_dir'],
                                   self._get_config()['project']['models']['main']['file'])
        except Exception as e:
            raise Exception('gen_code.yaml 文件内容出错，%s'%e)

    def init_project(self):
        '''
        产生一个包含 sample.mdj文件和gen_code_run.py单元的专案
        :return:
        '''
        gp = GenProject_Sample(r'%s' % self.args.get('umlfile'),
                        r'%s' % self.args.get('root_path',self.args.get('project_name')) )
        gp.gen_code(self.args.get('python_code',False))


    def gen_export(self):
        umlfile = self._get_umlfile()
        swg = GenSwagger(umlfile)
        swg.export_one_swgclass(self.args.get('umlclass'),umlfile)

    def gen_add(self):
        umlfile = self._get_umlfile()
        swg = GenSwagger(umlfile)
        swg.add_operation(self.args.get('swagger_package'), 
                          self.args.get('umlclass_operation'), 
                          self.args.get('http_method_type','get'))
 
    def gen_build(self):
        prj_type = self._get_apptype()
        umlfile = self._get_umlfile()
        prj_rootpath = self._get_rootpath()
        if prj_type =='flask':
            gp = GenProject_Flask(r'%s' % umlfile,
                                  r'%s' % prj_rootpath)
        elif prj_type =='aiohttp':
            gp = GenProject_Aiohttp(r'%s' % umlfile,
                                    r'%s' % prj_rootpath)
        else:
            raise Exception('不支持该project type(%s)'%prj_type)
        gp.gen_code()
        g = GenCode(umlfile, prj_rootpath)
        # 产生model
        g.model()

    def gen_upgrade(self):
        # logging.info(self.args)
        dir = self.args.get('dir','.')
        umlfile = self._get_umlfile()
        swg = ImportSwagger().impUMLModels(umlfile)
        if self.args.get('type','k8s')=='k8s':
            k8s = upgrade.Upgrade_k8s(dir,swg)
            k8s.merge_code()

@mcp.tool()
def init_project(project_name:str,project_type:str='flask',python_code:bool=False,root_path:str='.') -> str:
    '''
    此函数用于初始化一个Web框架专案。它会根据传入的参数创建专案的初始文件，
    包括UML模型文件、配置文件等，还可以选择生成gen_code_run.py单元。

    :param project_name: 专案的名称，用于指定专案的标识。
    :param project_type: 专案的类型，支持的类型有 'flask'、'aiohttp' 和 'fastapi'，默认为 'flask'。
    :param python_code: 一个布尔值，若为True，则会生成gen_code_run.py单元，默认为False。
    :param root_path: 项目的根目录路径，默认为当前目录 '.'。
    :return: 
    '''
    print("init_project",project_name,project_type,python_code,root_path)
    params = {"project_name": project_name, 
              "project_type": project_type, 
              "python_code": python_code,
              "root_path": root_path}
    gen_code = Gen_Code(params)
    gen_code.init_project()
    return f"初始化专案完成，专案名称为：{project_name}，专案类型为：{project_type}，是否生成gen_code_run.py单元：{python_code}"

@mcp.tool()
def build(root_path:str='.') -> str:
    '''
    产生项目相关的文件,包括run.py,config.py,models.py等,当UMLmodel或gen_code.yaml有变更时,需要重新执行,以生成代码
    :param root_path: 项目的根目录路径，默认为当前目录 '.'。
    :return:
    '''
    # 以下代码用于解析命令行参数，构建一个解析器对象，描述为初始化web框架的代码
    # 此函数的主要作用是在UML模型文件或配置文件发生变更时，重新生成项目相关文件
    # 调用Gen_Code类的gen_build方法来完成项目文件的生成操作
    gen_code = Gen_Code({"root_path": root_path})
    gen_code.gen_build()
    return "项目相关文件生成完成"

@mcp.tool()
def add(swagger_package:str,umlclass_operation:str,http_method_type:str='get',root_path:str='.') -> str:
    '''
    添加一个操作(umlclass_operation)到swagger相关类(swagger_package)

    此函数的主要作用是将指定的操作添加到Swagger相关类中。通过传入Swagger包类名、UML类操作名以及可选的HTTP方法类型，
    调用命令行参数解析和Gen_Code类的gen_add方法来完成操作的添加。

    :param swagger_package: Swagger包类的名称，例如 'employeemng'，用于指定要添加操作的Swagger类。
    :param umlclass_operation: UML类的操作名称，例如 'get_employee'，表示要添加的具体操作。
    :param http_method_type: 操作的HTTP方法类型，可选值有 'get'、'post'、'put'、'delete' 等，默认为 'get'。
    :param root_path: 项目的根目录路径，默认为当前目录 '.'。
    :return: 
    '''
    args = {'swagger_package': swagger_package,
            'umlclass_operation': umlclass_operation,
            'http_method_type': http_method_type,
            'root_path': root_path
            }
        
    gen_code = Gen_Code(args)
    gen_code.gen_add()
    return f"操作添加完成，Swagger包类为：{swagger_package}，UML类操作为：{umlclass_operation}，HTTP方法类型为：{http_method_type}"
@mcp.tool()
def export(umlclass:str,root_path:str='.') -> str:
    '''
    此函数的主要作用是将逻辑视图中的指定UML类生成Swagger类，包含GET、POST、PUT、DELETE等操作。
    当UML模型文件（UMLmodel）或项目配置文件（gen_code.yaml）有变更时，需要重新执行此函数，以确保生成最新的代码。
    :param root_path: 项目的根目录路径，默认为当前目录 '.'。
    :param umlclass: 逻辑视图中的UML类名称，例如 'employee'，用于指定要生成Swagger类的目标UML类。
    :return: 
    '''
    args = {'umlclass': umlclass,"root_path": root_path}
    gen_code = Gen_Code(args)
    gen_code.gen_export()
    return f"Swagger类生成完成，目标UML类为：{umlclass}"

@mcp.tool()
def upgrade(project_dir:str,upgrade_type:str='k8s',root_path:str='.') -> str:
    '''
    此函数的主要作用是对指定的项目进行升级操作，支持不同的升级类型。
    当UML模型文件（UMLmodel）或项目配置文件（gen_code.yaml）有变更时，需要重新执行此函数，以确保生成最新的代码。

    :param project_dir: 项目的目录路径，用于指定要升级的项目。
    :param upgrade_type: 升级的类型，可选值有 'k8s' 等，默认为 'k8s'。
    :param root_path: 项目的根目录路径，默认为当前目录 '.'。
    :return: 
    '''
    args = {'dir': project_dir, 'type': upgrade_type, 'root_path': root_path}
    gen_code = Gen_Code(args)
    gen_code.gen_upgrade()
    return f"项目升级完成，项目目录为：{project_dir}，升级类型为：{upgrade_type}"


if __name__ == "__main__":
    mcp.run(transport='stdio')

 