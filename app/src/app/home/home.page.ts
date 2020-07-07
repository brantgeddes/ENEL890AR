import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import * as d3 from 'd3';
import { timer } from 'rxjs';

@Component({
  selector: 'app-home',
  templateUrl: 'home.page.html',
  styleUrls: ['home.page.scss'],
})
export class HomePage implements OnInit {
  samples: any[];
  real: any[];
  imag: any[];
  amplitude: any[];
  phase: any[];

  constructor(
    private http: HttpClient
  ) {}

  ngOnInit() {
    const sub = timer(0, 1000).subscribe((x) => {
      this.http.get('http://207.195.41.157/api/samples').subscribe((result: any) => {
        this.samples = result.values;
        const data = this.samples.map((value, index) => ([ index, 3.3 * parseFloat(value) ]));
        this.draw('#samples-container', data, 'Amplitude', 'Time');
      });
      this.http.get('http://207.195.41.157/api/dft').subscribe((result: any) => {
        this.amplitude = result.amplitude;
        const data = this.amplitude.map((value, index) => ([ 245 * (index / 64), 3.3 * parseFloat(value) ]));
        this.draw('#dft-container', data, 'Amplitude', 'Frequency');
      });
    });
  }

  draw(container, data, ylabel, xlabel) {
    // set the dimensions and margins of the graph
    const margin = {top: 10, right: 30, bottom: 30, left: 60};
    const width = 460 - margin.left - margin.right;
    const height = 400 - margin.top - margin.bottom;

    // append the svg object to the body of the page
    d3.select(container).html('');
    const svg = d3.select(container)
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

    // Add X axis --> it is a date format
    const x = d3.scaleLinear()
      .domain([0, d3.max<[number, number], number>(data, d => d[0])])
      .range([0, width]);

    svg.append('g')
      .attr('transform', 'translate(0,' + height + ')')
      .call(d3.axisBottom(x));

    // Add Y axis
    const y = d3.scaleLinear()
      .domain([0, d3.max<[number, number], number>(data, d => d[1])])
      .range([ height, 0 ]);
    svg.append('g')
      .call(d3.axisLeft(y));

    // Add the line
    svg.append('g')
      .selectAll()
      .data(data)
      .enter()
      .append('circle')
      .attr('fill', 'black')
      .attr('cx', (d) => x(d[0]))
      .attr('cy', (d) => y(d[1]))
      .attr('r', 2);

    // text label for the x axis
    svg.append('text')
      .attr('transform',
            'translate(' + (width / 2) + ' ,' + (height + margin.top + 20) + ')')
      .style('text-anchor', 'middle')
      .text(xlabel);

    // text label for the y axis
    svg.append('text')
        .attr('transform', 'rotate(-90)')
        .attr('y', 0 - margin.left)
        .attr('x', 0 - (height / 2))
        .attr('dy', '1em')
        .style('text-anchor', 'middle')
        .text(ylabel);

  }

  calcPolar() {
    this.amplitude = this.real.map((x, i) => (x ** 2 + this.imag[i] ** 2) ** (1 / 2));
    this.phase = this.real.map((x, i) => Math.atan(this.imag[i] / x));
  }
}
