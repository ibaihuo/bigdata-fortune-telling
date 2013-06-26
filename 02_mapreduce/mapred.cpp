#include "mapreduce/mapreduce.h"
//用户map函数
class WordCounter : public Mapper {
public:
    virtual void Map(const MapInput& input) {
		const string& text = input.value();
		const int n = text.size();
		for (int i = 0; i < n; ) {
			//跳过前导空格
			while ((i < n) && isspace(text[i]))
				i++;
			// 查找单词的结束位置
			int start = i;
			while ((i < n) && !isspace(text[i]))
				i++;
			if (start < i)
				Emit(text.substr(start,i-start),"1");
        }
 
	}
 
};
 
REGISTER_MAPPER(WordCounter);
//用户的reduce函数
class Adder : public Reducer {
    virtual void Reduce(ReduceInput* input) {
		//迭代具有相同key的所有条目,并且累加它们的value
		int64 value = 0;
		while (!input->done()) {
			value += StringToInt(input->value());
			input->NextValue();
		}
		//提交这个输入key的综合
		Emit(IntToString(value));
	}
 
};
REGISTER_REDUCER(Adder);
int main(int argc, char** argv) {
	ParseCommandLineFlags(argc, argv);
	MapReduceSpecification spec;
	// 把输入文件列表存入"spec"
	for (int i = 1; i < argc; i++) {
		MapReduceInput* input = spec.add_input();
		input->set_format("text");
		input->set_filepattern(argv[i]);
		input->set_mapper_class("WordCounter");
	}
	//指定输出文件:
	// /gfs/test/freq-00000-of-00100
	// /gfs/test/freq-00001-of-00100
	// ...
	MapReduceOutput* out = spec.output();
	out->set_filebase("/gfs/test/freq");
	out->set_num_tasks(100);
	out->set_format("text");
	out->set_reducer_class("Adder");
	// 可选操作:在map任务中做部分累加工作,以便节省带宽
	out->set_combiner_class("Adder");
	// 调整参数: 使用2000台机器,每个任务100MB内存
	spec.set_machines(2000);
	spec.set_map_megabytes(100);
	spec.set_reduce_megabytes(100);
	// 运行它
	MapReduceResult result;
	if (!MapReduce(spec, &result)) abort();
	// 完成: 'result'结构包含计数,花费时间,和使用机器的信息
	return 0;
}
