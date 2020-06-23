""" Fichier permettant de réaliser une application web a partir de la simulation


"""

from ipywidgets import *
import matplotlib.pyplot as plt

from nbconvert.filters.markdown_mistune import markdown2html_mistune
import inspect


def _check_parameters_are_OK(parameters, plot_function):
    """ Check that ther parameters are argument of the plot_function"""
    if inspect.getfullargspec(plot_function).args[0]!='fig':
        raise Exception('First argument of "{f.__name__}" should be "fig"'.format(f=plot_function))
    func_parameters = inspect.getfullargspec(plot_function).args[1:]
    if set(parameters.keys())<=set(func_parameters):
        return
    raise Exception('The parameters {} are not all arguments of the function "{f.__name__}"'.format(set(parameters.keys()), f=plot_function))
    
def display_simulation_window(titre, parameters, plot_function, doc):
    _check_parameters_are_OK(parameters, plot_function)
    plt.close(titre)
    fig = plt.figure(titre)

    
    def update(**kwd):
        fig.clf()
        plot_function(fig=fig, **kwd)
        fig.canvas.draw()
        fig.canvas.flush_events()
        
    def observer(change):
        for k, w in parameters.items():
            w.continuous_update=False
        kwargs = {k:w.value for k,w in parameters.items()}
        update(**kwargs)
        for k, w in parameters.items():
            w.continuous_update=True

    for k,w in parameters.items():
        w.observe(observer, 'value')
        
    observer(None)

    doc += '\n-------------'
    w_doc = widgets.HTMLMath(
        value=markdown2html_mistune(doc),
        disabled=False,
        layout=Layout(width='250px')
    )
    
    param = []
    for elm in parameters.values():
        if isinstance(elm, (FloatSlider, IntSlider)):
            if "--" in elm.description:
                long_description, short_description = elm.description.split('--', 1)
            else:
                long_description, short_description = elm.description, ''
            param.append(Label(value=long_description))
            elm.description = short_description
        param.append(elm)
    
    left = VBox([w_doc]+param, layout=Layout(width='35%') )
    right = VBox([fig.canvas], layout=Layout(width='65%'))
    return HBox([left, right])
