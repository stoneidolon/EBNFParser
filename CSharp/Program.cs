﻿using System;
using System.IO;
namespace CSharp
{
    class Program
    {
        static void Main(string[] args)
        {
            // Gen source
            string source = File.ReadAllText("../selfexamine.ebnf");
            var (testfunc, path) = (Test.Manage.GetTest(args[0]), args[1]);
            File.WriteAllText(path, testfunc(source));
        }
    }
}