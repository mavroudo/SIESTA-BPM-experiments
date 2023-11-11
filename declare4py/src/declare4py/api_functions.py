from math import ceil

from .constraint_checkers import *
from .models import DeclModel


def check_trace_conformance(trace, model, consider_vacuity):
    rules = {"vacuous_satisfaction": consider_vacuity}

    # Set containing all constraints that raised SyntaxError in checker functions
    error_constraint_set = set()

    trace_results = {}

    for idx, constraint in enumerate(model.constraints):
        constraint_str = model.serialized_constraints[idx]
        rules["activation"] = constraint['condition'][0]

        if constraint['template'].supports_cardinality:
            rules["n"] = constraint['n']
        if constraint['template'].is_binary:
            rules["correlation"] = constraint['condition'][1]

        rules["time"] = constraint['condition'][-1]  # time condition is always at last position

        try:
            if constraint['template'] is Template.EXISTENCE:
                trace_results[constraint_str] = mp_existence(trace, True, set(constraint['activities']).pop(), rules)

            elif constraint['template'] is Template.ABSENCE:
                trace_results[constraint_str] = mp_absence(trace, True, set(constraint['activities']).pop(), rules)

            elif constraint['template'] is Template.INIT:
                trace_results[constraint_str] = mp_init(trace, True, set(constraint['activities']).pop(), rules)

            elif constraint['template'] is Template.EXACTLY:
                trace_results[constraint_str] = mp_exactly(trace, True, set(constraint['activities']).pop(), rules)

            elif constraint['template'] is Template.CHOICE:
                if len(list(constraint['activities'])) == 2:
                    acts = list(constraint['activities'])
                    trace_results[constraint_str] = mp_choice(trace, True, acts.pop(0), acts.pop(), rules)
                else:
                    print("Error it did not work to change direction")

            elif constraint['template'] is Template.EXCLUSIVE_CHOICE:
                if len(list(constraint['activities'])) == 2:
                    acts = list(constraint['activities'])
                    trace_results[constraint_str] = mp_exclusive_choice(trace, True, acts.pop(0), acts.pop(), rules)

            elif constraint['template'] is Template.RESPONDED_EXISTENCE:
                if len(list(constraint['activities'])) == 2:
                    acts = list(constraint['activities'])
                    trace_results[constraint_str] = mp_responded_existence(trace, True, acts.pop(0), acts.pop(), rules)



            elif constraint['template'] is Template.RESPONSE:
                if len(list(constraint['activities'])) == 2:
                    acts = list(constraint['activities'])
                    trace_results[constraint_str] = mp_response(trace, True, acts.pop(0), acts.pop(), rules)


            elif constraint['template'] is Template.ALTERNATE_RESPONSE:
                if len(list(constraint['activities'])) == 2:
                    acts = list(constraint['activities'])
                    trace_results[constraint_str] = mp_alternate_response(trace, True, acts.pop(0), acts.pop(), rules)



            elif constraint['template'] is Template.CHAIN_RESPONSE:
                if len(list(constraint['activities'])) == 2:
                    acts = list(constraint['activities'])
                    trace_results[constraint_str] = mp_chain_response(trace, True, acts.pop(0), acts.pop(), rules)



            elif constraint['template'] is Template.PRECEDENCE:
                if len(list(constraint['activities'])) == 2:
                    acts = list(constraint['activities'])
                    trace_results[constraint_str] = mp_precedence(trace, True, acts.pop(0), acts.pop(), rules)


            elif constraint['template'] is Template.ALTERNATE_PRECEDENCE:
                if len(list(constraint['activities'])) == 2:
                    acts = list(constraint['activities'])
                    trace_results[constraint_str] = mp_alternate_precedence(trace, True, acts.pop(0), acts.pop(), rules)



            elif constraint['template'] is Template.CHAIN_PRECEDENCE:
                if len(list(constraint['activities'])) == 2:
                    acts = list(constraint['activities'])
                    trace_results[constraint_str] = mp_chain_precedence(trace, True, acts.pop(0), acts.pop(), rules)



            elif constraint['template'] is Template.NOT_RESPONDED_EXISTENCE:
                if len(list(constraint['activities'])) == 2:
                    acts = list(constraint['activities'])
                    trace_results[constraint_str] = mp_not_responded_existence(trace, True, acts.pop(0), acts.pop(), rules)




            elif constraint['template'] is Template.NOT_RESPONSE:
                if len(list(constraint['activities'])) == 2:
                    acts = list(constraint['activities'])
                    trace_results[constraint_str] = mp_not_response(trace, True, acts.pop(0), acts.pop(), rules)


            elif constraint['template'] is Template.NOT_CHAIN_RESPONSE:
                if len(list(constraint['activities'])) == 2:
                    acts = list(constraint['activities'])
                    trace_results[constraint_str] = mp_not_chain_response(trace, True, acts.pop(0), acts.pop(), rules)



            elif constraint['template'] is Template.NOT_PRECEDENCE:
                if len(list(constraint['activities'])) == 2:
                    acts = list(constraint['activities'])
                    trace_results[constraint_str] = mp_not_precedence(trace, True, acts.pop(0), acts.pop(), rules)



            elif constraint['template'] is Template.NOT_CHAIN_PRECEDENCE:
                if len(list(constraint['activities'])) == 2:
                    acts = list(constraint['activities'])
                    trace_results[constraint_str] = mp_not_chain_precedence(trace, True, acts.pop(0), acts.pop(), rules)



        except SyntaxError:
            if constraint_str not in error_constraint_set:
                error_constraint_set.add(constraint_str)
                print('Condition not properly formatted for constraint "' + constraint_str + '".')

    return trace_results


def discover_constraint(log, constraint, consider_vacuity):
    # Fake model composed by a single constraint
    model = DeclModel()
    model.constraints.append(constraint)
    model.set_constraints()

    discovery_res = {}

    for i, trace in enumerate(log):
        trc_res = check_trace_conformance(trace, model, consider_vacuity)
        if not trc_res:  # Occurring when constraint data conditions are formatted bad
            break

        constraint_str, checker_res = next(iter(trc_res.items()))  # trc_res will always have only one element inside
        if checker_res.state == TraceState.SATISFIED:
            new_val = {(i, trace.attributes['concept:name']): checker_res}
            if constraint_str in discovery_res:
                discovery_res[constraint_str] |= new_val
            else:
                discovery_res[constraint_str] = new_val

    return discovery_res


def query_constraint(log, constraint, consider_vacuity, min_support):
    # Fake model composed by a single constraint
    model = DeclModel()
    model.constraints.append(constraint)

    sat_ctr = 0
    for i, trace in enumerate(log):
        trc_res = check_trace_conformance(trace, model, consider_vacuity)
        if not trc_res:  # Occurring when constraint data conditions are formatted bad
            break

        constraint_str, checker_res = next(iter(trc_res.items()))  # trc_res will always have only one element inside
        if checker_res.state == TraceState.SATISFIED:
            sat_ctr += 1
            # If the constraint is already above the minimum support, return it directly
            if sat_ctr / len(log) >= min_support:
                return constraint_str
        # If there aren't enough more traces to reach the minimum support, return nothing
        if len(log) - (i + 1) < ceil(len(log) * min_support) - sat_ctr:
            return None

    return None
