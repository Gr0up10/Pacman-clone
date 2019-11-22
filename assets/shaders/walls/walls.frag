#version 120
uniform vec4 rect;
uniform sampler2D texture;

varying vec4 main_color;

void main() {
    rect;
    vec2 uv = gl_TexCoord[0].st;

    float border = 1.;
    float st = 0.005;
    border *= length(texture2D(texture, uv+vec2(st, 0.)).rgb);
    border *= length(texture2D(texture, uv+vec2(-st, 0.)).rgb);
    border *= length(texture2D(texture, uv+vec2(0., st)).rgb);
    border *= length(texture2D(texture, uv+vec2(0., -st)).rgb);

    border = step(0.5, border);
    border = -(border-1.0) * length(texture2D(texture, uv).rgb);
    vec3 border_col = vec3(0., .0, 1.0);
    vec3 fcol = border_col*border;

    gl_FragColor = vec4(fcol, 1.);
}
