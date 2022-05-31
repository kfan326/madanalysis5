#pragma once

#include <iostream>
#include <map>
#include <vector>
#include <numeric>


#include "SampleAnalyzer/Commons/Service/LogService.h"
#include "SampleAnalyzer/Commons/Service/ExceptionService.h"

/*
namespace MDUtils {
	std::pair<MAfloat64,MAfloat64> CombineWithDistribution(std::map<MAuint32, MAfloat64> &weight_hash, std::string method){

		MAfloat64 sum = 0;
		int size = weight_hash.size();
		for(const auto &id_value : weight_hash){
			sum+=id_value.second;
		}

		if(method == "gaussian"){
			MAfloat64 mean = sum/size;
			MAfloat64 squarediff = 0;
			for(const auto &id_value : weight_hash){
				squarediff += pow(id_value.second-mean, 2);
			}
			return std::make_pair(mean, sqrt(squarediff/size));		
		}

		return std::make_pair(0 ,0);
	}
}
*/


namespace MA5
{

class WeightContainer {
	private:

		//hash map for id-value pair, last element stores id of last added element.
		std::map<MAuint32, MAfloat64> weights;

		std::pair<MAfloat64,MAfloat64> CombineWithDistribution(std::map<MAuint32, MAfloat64> &weight_hash, std::string method){

			MAfloat64 sum = 0;
			int size = weight_hash.size();
			for(const auto &id_value : weight_hash){
				sum+=id_value.second;
			}

			if(method == "gaussian"){
				MAfloat64 mean = sum/size;
				MAfloat64 squarediff = 0;
				for(const auto &id_value : weight_hash){
				squarediff += pow(id_value.second-mean, 2);
			}
			return std::make_pair(mean, sqrt(squarediff/size));		
			}	

			return std::make_pair(0 ,0);
		
		}	

	
	public:

		WeightContainer(){}
		~WeightContainer(){}

		void Reset(){
			weights.clear();
		}

		MAuint32 size() const {return weights.size();}
		
		
		MAbool Add(MAuint32 id, MAfloat64 value){
			weights[id] = value;
			bool insert_success = weights.find(id) != weights.end();
			if(!insert_success) {
			
				throw EXCEPTION_WARNING("The Weight '" + std::to_string(id) +
                                "' is defined at two times. Redundant values are skipped.","",0);
			}
			return insert_success;		
		}

		const std::map<MAuint32, MAfloat64>& GetWeights() const {return weights;}

		const MAfloat64& GetWeight (const MAuint32 id) const {
			return weights.find(id)->second;
		}

		const MAfloat64& operator[](const MAuint32 id) const {return GetWeight(id);}

		void operator*=(const MAfloat64 multiple){
			for(auto &id_value : weights){
				id_value.second *= multiple;
			}
		}

	
		void operator+=(const MAfloat64 input){
			for(auto &id_value : weights){
				id_value.second += input;
			}
		}

		void Print() const{
			for(const auto &id_value : weights){
				INFO << "ID=" << id_value.first << " : " << id_value.second << endmsg;
			}
		}
		
		
		std::pair<MAfloat64, MAfloat64> CombineWeights(const std::string method){	
			return CombineWithDistribution(weights, method);
		}
		

	};

}


