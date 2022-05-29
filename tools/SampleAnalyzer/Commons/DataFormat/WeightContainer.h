#pragma once

#include <iostream>
#include <unordered_map>
#include <vector>
#include <numeric>

#include "SampleAnalyzer/Commons/Service/LogService.h"
#include "SampleAnalyzer/Commons/Service/ExceptionService.h"

namespace MDUtils {
	std::pair<MAfloat64,MAfloat64> CombineWithDistribution(std::unordered_map<MAuint32, MAfloat64> &weight_hash, std::string method){

		MAuint32 sum = 0;
		int size = weight_hash.size();
		for(const auto &[id, value] : weight_hash){
			sum+=value;
		}

		if(method == "gaussian"){
			MAfloat64 mean = sum/size;
			MAfloat64 squarediff = 0;
			for(const auto &[id, value] : weight_hash){
				squarediff += pow(value-mean, 2);
			}
			return std::make_pair(mean, sqrt(squarediff/size));		
		}	
	}
}


namespace MA5
{

class WeightContainer {
	private:

		//hash map for id-value pair, last element stores if of last added element.
		std::unordered_map<MAuint32, MAfloat64> weights;
		MAuint32 last_element = -1;

	public:

		WeightContainer(){}
		~WeightContainer(){}

		void Reset(){
			weights.clear();
			last_element = -1;
		}
		
		
		MAbool Add(MAuint32 id, MAfloat64 value){
			weights[id] = value;
			last_element = id;
		}

		const std::unordered_map<MAuint32, MAfloat64>& GetWeights() {return weights;}

		MAfloat64 GetWeight(const MAuint32 id) const {
			if(weights.find(id) != weights.end()){
				return weights[id];
			}
			else {
				throw EXCEPTION_ERROR("The Weight '" + to_string(id) + "' is not defined. Return null value.", "", 0);
			}
		}

		MAfloat64 operator[](const MAuint32 id) const {return GetWeight[id];}

		void operator*=(const MAfloat64 multiple){
			for(auto &[id, value] : weights){
				value *= multiple;
			}
		}

		WeightContainer& operator* (const MAfloat64 multiple) {
			for(auto &[id, value] : weights){
				value *= multiple;
			}
			return *this;

		}

		void operator+=(const MAfloat64 input){
			for(auto &[id, value] : weights){
				value += input;
			}
		}

		WeightContainer& operator+ (const MAfloat64 input) {
			for(auto &[id, value] : weights){
				value += input;
			}
			return *this;

		}

		void Print() const{
			for(const auto &[id, value] : weights){
				INFO << "ID=" << id << " : " << value << endmsg;
			}
		}

		MDfloat64 lastValue(){
			if(last_element != -1) {return weights[last_element];}
			else {
				throw EXCEPTION_ERROR("There are no weights to return!")
			}
		}

		std::pair<MAfloat64, MAfloat64> CombineWeights(const std::string method){	
			return weights.size()>0?MDUtils::CombineWithDistribution(weights, method):std::make_pair(0,0);
		}

	};

}


