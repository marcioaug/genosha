/*
 * This file was automatically generated by EvoSuite
 * Mon Sep 17 19:04:19 GMT 2018
 */

package br.ufal.ic.masg.operations;

import org.junit.Test;
import static org.junit.Assert.*;
import br.ufal.ic.masg.operations.NotEqual;
import org.evosuite.runtime.EvoRunner;
import org.evosuite.runtime.EvoRunnerParameters;
import org.junit.runner.RunWith;

@RunWith(EvoRunner.class) @EvoRunnerParameters(mockJVMNonDeterminism = true, useVFS = true, useVNET = true, resetStaticState = true, separateClassLoader = true, useJEE = true) 
public class NotEqual_ESTest extends NotEqual_ESTest_scaffolding {

  @Test(timeout = 4000)
  public void test0()  throws Throwable  {
      NotEqual notEqual0 = new NotEqual();
      boolean boolean0 = notEqual0.function(685, 1316);
      assertTrue(boolean0);
  }

  @Test(timeout = 4000)
  public void test1()  throws Throwable  {
      NotEqual notEqual0 = new NotEqual();
      boolean boolean0 = notEqual0.function(363, 102);
      assertTrue(boolean0);
  }

  @Test(timeout = 4000)
  public void test2()  throws Throwable  {
      NotEqual notEqual0 = new NotEqual();
      boolean boolean0 = notEqual0.function(0, 0);
      assertFalse(boolean0);
  }
}
