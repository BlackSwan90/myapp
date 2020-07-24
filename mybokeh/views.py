from django.shortcuts import render, render_to_response
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models.widgets import Select
from django.template import RequestContext



from .utils import *
import global_storage

global_storage.get_selector_list()

def view_bk(request):

	context_selector_list = global_storage.selector_list
	context_demo_selection = get_demo_selection()

	demo_plot_bk = get_demo_plot_bk()
	script_demo_bk, div_demo_bk = components(demo_plot_bk)
	context_bk_demo = {'script': script_demo_bk, 'div': div_demo_bk}

	context = {
		**context_bk_demo,
		**context_selector_list,
		**context_demo_selection,
	}

	if request.method == 'POST':
		selected_symbol  = request.POST.get('symbol_selector')
		selected_period = request.POST.get('period_selector')
		selected_freqtype = request.POST.get('freqtype_selector')
		period_number = request.POST.get('period_number')
		selected_freqnum = request.POST.get('freqnum_selector')
		manual_selection = request.POST.get('axis_limit')
		price_range = request.POST.get('price_range')
		time_min = request.POST.get('time_min')
		time_max = request.POST.get('time_max')
		time_range = [time_min, time_max]

		context_bk_update = {
			'selected_symbol': selected_symbol,
			'selected_period': selected_period,
			'period_number': period_number,
			'selected_freqtype': selected_freqtype,
			'selected_freqnum': selected_freqnum,
			'manual_selection': manual_selection,
			'price_range': price_range,
			'time_range': time_range,
		}

		plot_bk = get_plot_bk(**context_bk_update)

		script_bk, div_bk = components(plot_bk)

		context = {
			'script': script_bk,
			'div': div_bk,
			**context_selector_list,
			**context_bk_update,
		}

		return render_to_response('templates/css_test4.html',context)

	return render_to_response('templates/css_test4.html',context)


