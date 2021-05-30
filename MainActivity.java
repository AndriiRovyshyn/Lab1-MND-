package com.example.lab2a;

import androidx.appcompat.app.AppCompatActivity;

import android.annotation.SuppressLint;
import android.os.Bundle;

import androidx.appcompat.app.AppCompatActivity;

import android.view.View;
import android.widget.AdapterView;
import android.widget.Button;
import android.widget.TextView;
import android.view.View;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.textfield.TextInputEditText;


public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
    }


    @SuppressLint("SetTextI18n")
    public void Start(View view){
        long start = System.currentTimeMillis();

        TextInputEditText data0 = findViewById(R.id.editText1);
        TextInputEditText data1 = findViewById(R.id.editText2);
        TextInputEditText data2 = findViewById(R.id.editText3);

        TextView res = findViewById(R.id.textView6);

        double[] data = {0.01, 0.1, 1000};

        data[0] = Double.parseDouble(data0.getText().toString());
        data[1] = Double.parseDouble(data1.getText().toString());
        data[2] = Double.parseDouble(data2.getText().toString());

        double stage = 4;
        double W1 = 0;
        double W2 = 0;

        double[][] points = { {0.0, 6.0}, {1.0, 5.0}, {3.0, 3.0}, {2.0, 4.0} };

        int count = 0;
        int succ = 0;
        int curP = -1;
        int hod = 0;
        while (count <= data[2]) {
            if (succ >= 4) {
                break;
            }

            curP = hod%4;
            hod++;

            double test = W1 * points[curP][0] + W2 * points[curP][1];

            if (((curP < 2) && test >= stage) || ((curP >= 2) && test < stage)) {
                succ++;
                continue;
            } else {
                succ = 0;
            }

            double delta = stage - test;

            W1 += delta * points[curP][0] * data[0];
            W2 += delta * points[curP][1] * data[0];

            W1 = Math.ceil(W1 * Math.pow(10, 7)) / Math.pow(10, 7);
            W2 = Math.ceil(W2 * Math.pow(10, 7)) / Math.pow(10, 7);

            if (System.currentTimeMillis() - start >= data[1]) {
                break;
            }

            count++;
        }

        res.setText("Значення параметрів:\n" +
                "W1 = " + W1 + "\nW2 = " + W2 +"\nЧас виконання: " +
                (System.currentTimeMillis() - start) + " мс");
    }
}
