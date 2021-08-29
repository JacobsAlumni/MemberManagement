import { generate, ChartConfiguration, Primitive } from 'c3';
import { format as d3_format } from 'd3-format';
import 'c3/c3.css';

const format_value = d3_format('') as (value: Primitive | number | undefined) => string;
const format_ratio = d3_format('.1%') as (value: Primitive | number | undefined) => string;

function make_pie_chart(
    element: HTMLElement, values: Record<string, number>, columns: Array<[string, string]> | Array<string>,
    column_labels: Record<string, string> | ((name: string) => string) | undefined = undefined,
    extra_config: Partial<ChartConfiguration> | undefined = undefined
) {

    let label_func: (name: string) => string;
    if (column_labels === undefined) {
        label_func = (name: string) => name;
    } else if (typeof column_labels === 'function') {
        label_func = column_labels;
    } else {
        label_func = (name: string) => {
            if (Object.prototype.hasOwnProperty.call(column_labels, name)) {
                return column_labels[name];
            }
            return name;
        }
    }

    // check if we want to have automatic colors
    const is_auto_color = columns.length > 0 && typeof columns[0] === 'string';
    let names: Array<string>;
    let names_and_colors: Array<[string, string]>;
    if (is_auto_color) {
        names = columns as Array<string>;
        names_and_colors = names.map(c => [c, '']); // unused
    } else {
        names_and_colors = columns as Array<[string, string]>;
        names = names_and_colors.map(([name, color]) => name);
    }

    // compute labels for the data (and reverse labels)
    const labels: Record<string, string> = {};
    const reverse_labels: Record<string, string> = {};
    names.forEach(name => {
        const the_name = label_func(name);
        const the_label = `${the_name}: ${format_value(values[name])}`;
        labels[name] = the_label;
        reverse_labels[the_label] = name;
    });

    // setup basic configuration
    const config: ChartConfiguration = {
        bindto: element,
        data: {
            /* columns: [] */
            /* colors: {} */
            type: 'pie',
        },
        pie: {
            label: {
                format: (value, ratio, id) => label_func(reverse_labels[id]),
            },
        },
        tooltip: {
            format: {
                value: (value, ratio, id) => `${format_ratio(ratio)}`,
            }
        },
        legend: { position: 'right' },
    }

    // setup data and colors
    if (is_auto_color) {
        config.data.columns = names.map(name => [labels[name], values[name]]);
    } else {
        config.data.colors = {};
        config.data.columns = names_and_colors.map(([key, color]) => {
            const label = labels[key]
            config.data.colors![label] = color;
            return [label, values[key]];
        });
    }

    // add extra config
    if (extra_config !== undefined) {
        Object.assign(config, extra_config);
    }

    return generate(config);
}

const totalElement = document.getElementById('total') as HTMLSpanElement;

const setupElement = document.getElementById('setup') as HTMLDivElement;
const approvalElement = document.getElementById('approval') as HTMLDivElement;
const autoElement = document.getElementById('auto') as HTMLDivElement;

const tierElement = document.getElementById('tier') as HTMLDivElement;
const categoryElement = document.getElementById('category') as HTMLDivElement;

const degreeElement = document.getElementById('degree') as HTMLDivElement;
const graduationElement = document.getElementById('graduation') as HTMLDivElement;

const majorElement = document.getElementById('major') as HTMLDivElement;
const collegeElement = document.getElementById('college') as HTMLDivElement;

const genderElement = document.getElementById('gender') as HTMLDivElement;
const atlasElement = document.getElementById('atlas') as HTMLDivElement;

const COLORS_YES_NO = [['yes', '#008000'], ['no', '#800080']] as Array<[string, string]>;

function write_stats(stats: PortalStats) {
    totalElement.innerText = format_value(stats.total);

    make_pie_chart(setupElement, stats.setup, COLORS_YES_NO);
    make_pie_chart(approvalElement, stats.approval, COLORS_YES_NO);
    make_pie_chart(autoElement, stats.autocreated, COLORS_YES_NO);

    make_pie_chart(tierElement, stats.tier, Object.keys(stats.tier),
        (name: string) => name.split(/\s/)[0],
    );
    make_pie_chart(categoryElement, stats.category, Object.keys(stats.category),
        (name: string) => name.split(/\s/)[0],
    );

    make_pie_chart(degreeElement, stats.degree, Object.keys(stats.degree),
        {
            'Foundation Year': 'FY',
            'Bachelor of Arts': 'BA',
            'Bachelor of Science': 'BSc',
            'Master of Arts': 'MA',
            'Master of Science': 'MSc',
        }
    );
    make_pie_chart(graduationElement, stats.graduation, Object.keys(stats.graduation),
        (name: string) => name.startsWith('Class') ? name.split(/\s/).reverse()[0] : 'Other'
    );

    make_pie_chart(majorElement, stats.major, Object.keys(stats.major),
        {
            'Other (Please specify in comments)': 'Other',
        },
        { legend: { show: false, } },
    );
    make_pie_chart(collegeElement, stats.college, [
        ['Nordmetall', 'yellow'],
        ['Krupp', 'red'],
        ['Mercator', 'blue'],
        ['College III', 'darkgreen'],
        ['College V', 'black']
    ]);

    make_pie_chart(genderElement, stats.gender, [
        ['Prefer not to say', 'black'],
        ['Non-binary', 'yellow'],
        ['Female', 'red'],
        ['Male', 'blue'],
    ]);
    make_pie_chart(atlasElement, stats.atlas, COLORS_YES_NO);
}

document.addEventListener('DOMContentLoaded', () => {
    write_stats(window.stats);
    console.log('Done!');
});