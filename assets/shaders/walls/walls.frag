#version 120
uniform vec4 rect;
uniform sampler2D texture;

varying vec4 main_color;

void main() {
    float coef = rect.w/rect.z;
    vec2 uv = gl_TexCoord[0].st;

    float border = 1.;
    float st = 0.011; //border radius
    float en = 0.008;
    border *= length(texture2D(texture, uv+vec2(st * coef, 0.)).rgb);
    border *= length(texture2D(texture, uv+vec2(-st * coef, 0.)).rgb);
    border *= length(texture2D(texture, uv+vec2(0., st)).rgb);
    border *= length(texture2D(texture, uv+vec2(0., -st)).rgb);
    border *= length(texture2D(texture, uv+vec2(-st * coef, -st)).rgb);
    border *= length(texture2D(texture, uv+vec2(st * coef, -st)).rgb);
    border *= length(texture2D(texture, uv+vec2(st * coef, st)).rgb);
    border *= length(texture2D(texture, uv+vec2(-st * coef, st)).rgb);

    float s_border = 1.0;
    s_border *= length(texture2D(texture, uv+vec2(en * coef, 0.)).rgb);
    s_border *= length(texture2D(texture, uv+vec2(-en * coef, 0.)).rgb);
    s_border *= length(texture2D(texture, uv+vec2(0., en)).rgb);
    s_border *= length(texture2D(texture, uv+vec2(0., -en)).rgb);
    s_border *= length(texture2D(texture, uv+vec2(-en * coef, -en)).rgb);
    s_border *= length(texture2D(texture, uv+vec2(en * coef, -en)).rgb);
    s_border *= length(texture2D(texture, uv+vec2(en * coef, en)).rgb);
    s_border *= length(texture2D(texture, uv+vec2(-en * coef, en)).rgb);

    s_border = step(0.5, s_border);
    border = step(0.5, border);
    //border = s_border;
    border = -(border-1.0) * length(texture2D(texture, uv).rgb) * s_border;

    vec3 border_col = vec3(0., .0, 1.0);
    vec3 fcol = border_col*border;

    gl_FragColor = vec4(fcol, 1.);
}
