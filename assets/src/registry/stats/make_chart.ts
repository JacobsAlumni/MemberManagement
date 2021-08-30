import { generate } from 'c3';
import type { ChartConfiguration, Primitive, ChartType, DataSeries, DataPoint } from 'c3';
import { format as d3_format } from 'd3-format';
import type { RGBColor, HSLColor } from 'd3';
import { schemeCategory10 } from 'd3-scale-chromatic';
import 'c3/c3.css';

export const format_value = d3_format('') as (value: Primitive | number | undefined) => string;
export const format_ratio = d3_format('.1%') as (value: Primitive | number | undefined) => string;

/** makes a simple bar chart */
export default function make_chart(
    type: ChartType, element: HTMLElement, values: Record<string, number>, columns: Array<[string, string]> | Array<string>,
    column_labels: Record<string, string> | ((name: string) => string) | undefined = undefined,
    extra_config: Partial<ChartConfiguration> | ((config: ChartConfiguration) => ChartConfiguration) | undefined = undefined
) {
    const label_func = make_label_func(column_labels);

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
    let config: ChartConfiguration = {
        bindto: element,
        data: {
            /* columns: [] */
            /* colors: {} */
            type: type
        },
        tooltip: {
            format: {
                value: (value, ratio, id) => `${format_ratio(ratio)}`,
            }
        },
        legend: { position: 'right' },
    }

    switch (type) {
        case 'pie':
            config['pie'] = {
                label: {
                    format: (value, ratio, id) => label_func(reverse_labels[id]),
                }
            };
            break;
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

    // apply extra configuration
    if (extra_config !== undefined) {
        if (typeof extra_config === 'function') {
            config = extra_config(config);
        } else {
            config = Object.assign(config, extra_config);
        }
    }

    return generate(config);
}

interface BarSeriesOptions {
    /* should empty values be culled and removed? */
    cull?: boolean;
    /* sort by label or count */
    sort?: 'label' | 'count';
    /* when true, hide tick labels! */
    noticks?: boolean;
}

export function as_bar_series(options: BarSeriesOptions): (config: ChartConfiguration) => ChartConfiguration {
    return (config: ChartConfiguration) => {
        if (config.data.type !== 'pie') {
            throw new Error('Only a PieChart can be turned into a Bar Series');
        }
        config.data.type = 'bar';

        let columns = config.data.columns!;
        if (options.cull ?? false) {
            columns = columns.filter(x => x[1] !== 0);
        }
        if (options.sort === 'count') {
            columns = columns.sort((b, a) => (a[1] as number) - (b[1] as number));
        }
        if (options.sort === 'label') {
            columns = columns.sort((b, a) => (a[0] as unknown as number) - (b[0] as unknown as number));
        }

        // transpose the labels and colors!
        const labels = columns.map(x => x[0]) as Array<string>;
        const counts = columns.map(x => x[1]) as Array<number>;

        config.data.x = 'labels';
        config.data.columns = [['labels', ...labels], ['counts', ...counts]];

        // enforce a category plot, and setup proper labels!
        const original_label_format = config?.pie?.label?.format;
        config.axis = {
            x: {
                type: 'category',
                tick: {
                    format: (index: number | Date) => {
                        if (options.noticks || typeof index !== 'number') {
                            return '';
                        }
                        if (!original_label_format) {
                            return labels[index];
                        }

                        const id = labels[index];
                        const value = counts[index];
                        const ratio = value / total;
                        return original_label_format(value, ratio, id);
                    },
                },
            }
        };
        config.legend = { show: false };

        const the_colors = config.data.colors ?? {};
        const get_color_by_index = (index: number): string | RGBColor | HSLColor => {
            const label = labels[index];
            const color = the_colors[label];
            if (color === undefined) {
                return schemeCategory10[index % schemeCategory10.length];
            }
            if (typeof color === 'function') {
                return color(labels[index]);
            }
            return color;
        }

        // setup a faked tooltip!
        const original_tooltip_title = config.tooltip?.format?.title;
        const original_tooltip_name = config.tooltip?.format?.name;
        const original_tooltip_value = config.tooltip?.format?.value;

        const total = counts.reduce((v, c) => v + c);
        let color_hack_index: number | undefined; // set to the last index, so that we can fake a proper index!
        config.tooltip!.format = {
            // store the index (for the color below), then do the original title
            title: (x: Primitive, index: number) => {
                color_hack_index = index;
                return original_tooltip_title ? original_tooltip_title(x, index) : '';
            },
            // use the proper label!
            name: (name: string, ratio: number | undefined, id: string, index: number) => {
                const label = labels[index];
                if (!original_tooltip_name) return label;

                const count_value = counts[index];
                const count_ratio = count_value / total;
                return original_tooltip_name(label, count_ratio, label, index);
            },

            // call the original value formatter
            value: (value: Primitive, ratio: number | undefined, id: string, index: number) => {
                if (!original_tooltip_value) return undefined;

                const count_value = counts[index];
                const count_ratio = count_value / total;
                return original_tooltip_value(count_value, count_ratio, labels[index], index);
            },
        }

        // setup colors
        config.data.color = function (color: string, d: string | DataSeries | DataPoint) {
            let index;
            if (typeof d === 'string' || !d.hasOwnProperty('x')) {
                if (color_hack_index === undefined) {
                    return color;
                }
                index = color_hack_index;
                color_hack_index = undefined;
            } else {
                index = (d as DataPoint).index;
            }
            return get_color_by_index(index);
        }

        return config;
    }
}


type LABEL_FUNCTION = (name: string) => string;

function make_label_func(column_labels: Record<string, string> | LABEL_FUNCTION | undefined): LABEL_FUNCTION {
    if (column_labels === undefined) {
        return (name: string) => name;
    } else if (typeof column_labels === 'function') {
        return column_labels;
    } else {
        return (name: string) => {
            if (Object.prototype.hasOwnProperty.call(column_labels, name)) {
                return column_labels[name];
            }
            return name;
        }
    }
}