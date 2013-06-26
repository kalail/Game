#version 330

in vec4 position;

// layout(location = 0) in vec4 vert;

// uniform mat4 projection;
// uniform mat4 view;
// uniform mat4 model;


void main()
{
    gl_Position = position;
    // gl_Position = projection * view * model * vert;
}


// uniform mat4 u_mvpMatrix;

// attribute vec4 a_position;
// attribute vec2 a_texCoord; 

// varying vec2 v_texCoord;

// void main() {
//     v_texCoord = a_texCoord;
//     gl_Position = u_mvpMatrix * a_position;
// }