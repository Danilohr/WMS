# WMS: Do que se trata o programa?
O WMS avisa automaticamente os alunos de um grupo do Whatsapp sobre as atividades pendentes.

Durante o decorrer dos anos estudando no [CEFET-MG](https://www.cefetmg.br), me deparei com um problema que poderia ser resolvido por meio de meus conhecimentos em programação.
Diariamente, eu e os demais alunos tinham que acessar dois portais usados pela instituição para troca de notícias e envio de atividades. Estes portais não tinham um sistema de login que salvava credenciais do usuário por meio de cookies, isso fazia com que todo acesso aos portais de atividades exigia o preenchimento dos campos de login e senha (que são sempre os mesmos em ambos os sites).


Para facilitar a visualização das tarefas de escola, fiz este programa em Python. Ele acessa ambos os portais com seu login e senha, e por meio do Web Scrapping retorna uma lista ordenada por data de envio de todas as tarefas. Esta lista pode ser enviada pelo Whatsapp em algum chat selecionado, porém é necessário ter o [Whatsapp Business](https://business.whatsapp.com).
- Portais: [Moodle](https://ava.cefetmg.br/calendar/view.php?view=upcoming), [Sigaa](https://sig.cefetmg.br/sigaa/verTelaLogin.do)
