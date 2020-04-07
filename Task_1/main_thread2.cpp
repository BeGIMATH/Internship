#include <iostream>                   // for std::cout
#include <boost/cstdint.hpp>      // for boost::boost::uint64_t
#include <boost/chrono.hpp>           // for boost::chrono::high_resolution_clock
#include <boost/thread.hpp>           // for boost::thread and boost::mutex
#include <vector>                 // for std::vector
#include <cassert>                    // for assert
 
#define TRACE
 
#ifdef TRACE
 
boost::mutex coutmutex;
#endif

std::vector<boost::uint64_t *> part_sums;
const int max_sum_item = 1000000000;
const int threads_to_use = 8;
 
void do_partial_sum(boost::uint64_t *final, int start_val, int sums_to_do)
{
#ifdef TRACE
    coutmutex.lock();
    std::cout << "Start: TID " << boost::this_thread::get_id() << " starting at " << start_val << ", workload of " << sums_to_do << " items" << std::endl;
    coutmutex.unlock();
 
    boost::chrono::high_resolution_clock::time_point start = boost::chrono::high_resolution_clock::now();
#endif
 
    boost::uint64_t sub_result = 0;
 
    for (int i = start_val; i < start_val + sums_to_do; i++)
        sub_result += i;
 
    *final = sub_result;
 
#ifdef TRACE
    boost::chrono::high_resolution_clock::time_point end = boost::chrono::high_resolution_clock::now();
 
    coutmutex.lock();
    std::cout << "End  : TID " << boost::this_thread::get_id() << " with result " << sub_result << ", time taken "
        << (end - start).count() * ((double) boost::chrono::high_resolution_clock::period::num / boost::chrono::high_resolution_clock::period::den) << std::endl;
    coutmutex.unlock();
#endif
}
 
int main()
{
  part_sums.clear();
 
  for (int i = 0; i < threads_to_use; i++)
    part_sums.push_back(new boost::uint64_t(0));
 
  std::vector<boost::thread *> t;
 
  int sums_per_thread = max_sum_item / threads_to_use;
 
  boost::chrono::high_resolution_clock::time_point start = boost::chrono::high_resolution_clock::now();
 
  for (int start_val = 0, i = 0; start_val < max_sum_item; start_val += sums_per_thread, i++)
  {
    // Lump extra bits onto last thread if work items is not equally divisible by number of threads
    int sums_to_do = sums_per_thread;
 
    if (start_val + sums_per_thread < max_sum_item && start_val + sums_per_thread * 2 > max_sum_item)
        sums_to_do = max_sum_item - start_val;
 
    t.push_back(new boost::thread(do_partial_sum, part_sums[i], start_val, sums_to_do));
    
    if (sums_to_do != sums_per_thread)
        break;
  }
 
  for (int i = 0; i < threads_to_use; i++)
    t[i]->join();
 
  boost::uint64_t result = 0;
 
  for (std::vector<boost::uint64_t *>::iterator it = part_sums.begin(); it != part_sums.end(); ++it)
      result += **it;
 
  boost::chrono::high_resolution_clock::time_point end = boost::chrono::high_resolution_clock::now();
 
  for (int i = 0; i < threads_to_use; i++)
  {
    delete t[i];
    delete part_sums[i];
  }
 
  assert(result == boost::uint64_t(499999999500000000));
 
  std::cout << "Result is correct" << std::endl;
 
  std::cout << "Time taken: " << (end - start).count() * ((double) boost::chrono::high_resolution_clock::period::num / boost::chrono::high_resolution_clock::period::den) << std::endl;
}