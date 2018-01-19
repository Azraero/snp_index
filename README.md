# snp index
snp index 是一个使用 [ jquery](http://www.juery.com) + [bootstrap](http://www.bootstrap.com) 作为前端框架，[flask](http://www.flask.org) 作为后端框架的简单 web application.
## 基本功能
- Gene Variation:
	- search gene by regin: 根据染色体的区域搜索 gene 的 snp;
	- search gene by name: 根据 gene 的名字进行搜索 snp;
- Gene Expression:
	- search expression by gene: 根据 gene 名字（可以输入多个查询 gene）查询 gene 的表达;
- Tools:
	- blast: 使用开源的 [ViroBLAST](https://els.comotion.uw.edu/licenses/1) 进行在线的 blast 分析;
	- search locus identidier gene: 获得查询 gene 的基本信息表格;
- Snp Index:
    - snp index plot: 利用 [bedtools](http://bedtools.readthedocs.io/en/latest/) 和 [ggplot2](https:www.ggplot2.org)
    按照输入的比较组信息和染色体进行 snp 位点的可视化;

## 关于安装与运行
首先保证已经正确安装 `python2.7.12` 或在其它 `python2.7` 的运行环境和 `pip` 安装工具,然后执行以下代码:
```sh
git clone https://www.github.com/jamebluntcc/snp_index.git
pip install -r requirements.txt
python manager.py runserver
```

## Changelog
1.23 (13/11/2017)
- add snp index plot.

1.24 (01/12/2017)
- refactor app and add snp index plot.

1.25 (05/12/2017)
- app download snp index zip and map samples and auth system.

1.26 (26/12/2017)
- add celery,search all snp variation and mail remind user.

2.00 (19/01/2018)
- refactor auth system, mail verify and so on. 

