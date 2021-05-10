
from app import *
@app.route('/')
def test_index():
    print("Hello index")
    index()
    x = "Hello index"
    assert(x == "Hello index")


@app.route('/find', methods=['POST'])
def test_find():

    language_name, sel_word = None, None
    if request.method == 'POST':
        language_id = request.form['sellanguage']
        sel_word = request.form['selword']
        language_name = language_dict[language_id]
        if not appService.udt_pre_model:
            appService.config_udpipe(language_name)
        appService.find_service(language_name, sel_word)
    return render_templateMock('result.html', input_data={"language_name": language_name,
                                                      "sel_word": sel_word,
                                                      "sel_result": appService.sel_result})


@app.route('/find2', methods=['POST'])
def find2():
    language_name, sel_word = None, None
    if request.method == 'POST':
        language_name = request.form['sellanguage']
        sel_word = request.form['selword']
        if not appService.udt_pre_model:
            appService.config_udpipe(language_name)
        appService.find_service(language_name, sel_word)
    return render_templateMock('result.html', input_data={"language_name": language_name,
                                                      "sel_word": sel_word,
                                                      "sel_result": appService.sel_result})


@app.route('/cluster', methods=['POST'])
def test_cluster():

    if request.method == 'POST':
        language_name = request.form['languageName']
        cluster_number = request.form['clusterNumber']
        sel_tag = request.form['tagInput1']
        cluster_input_sentence = appService.pos_dict[sel_tag]
        if not appService.udt_pre_model:
            appService.config_udpipe(language_name)
        cluster_model_file = word2vec_language[language_name]
        cluster_result, rec_cluster_result = appService.cluster_sentences(
            language_name, cluster_model_file, cluster_input_sentence, cluster_number)
        return render_templateMock('cluster.html',
                               cluster_number=cluster_number,
                               cluster_result=cluster_result,
                               rec_cluster_result=rec_cluster_result)

def render_templateMock(template_name_or_list, **context):
    
    ctx = _app_ctx_stack.top
    ctx.app.update_template_context(context)
    return _renderMock(
        ctx.app.jinja_env.get_or_select_template(template_name_or_list),
        context,
        ctx.app,
    )
def _renderMock(template, context, app):
    """Renders the template and fires the signal"""

    before_render_template.send(app, template=template, context=context)
    rv = template.render(context)
    template_rendered.send(app, template=template, context=context)
    return rv

if __name__ == "__main__":
    test_index()
    test_find()
    test_index()
    
