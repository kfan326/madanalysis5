////////////////////////////////////////////////////////////////////////////////
//
//  Copyright (C) 2012-2022 Jack Araz, Eric Conte & Benjamin Fuks
//  The MadAnalysis development team, email: <ma5team@iphc.cnrs.fr>
//
//  This file is part of MadAnalysis 5.
//  Official website: <https://launchpad.net/madanalysis5>
//
//  MadAnalysis 5 is free software: you can redistribute it and/or modify
//  it under the terms of the GNU General Public License as published by
//  the Free Software Foundation, either version 3 of the License, or
//  (at your option) any later version.
//
//  MadAnalysis 5 is distributed in the hope that it will be useful,
//  but WITHOUT ANY WARRANTY; without even the implied warranty of
//  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
//  GNU General Public License for more details.
//
//  You should have received a copy of the GNU General Public License
//  along with MadAnalysis 5. If not, see <http://www.gnu.org/licenses/>
//
////////////////////////////////////////////////////////////////////////////////

#ifndef MADANALYSIS5_RECLUSTER_H
#define MADANALYSIS5_RECLUSTER_H

// FastJet headers
#include "fastjet/contrib/Recluster.hh"

// SampleAnalyser headers
#include "SampleAnalyzer/Interfaces/fastjet/ClusterBase.h"

using namespace std;

namespace MA5 {
    namespace Substructure {
        class Recluster : public ClusterBase{

            // -------------------------------------------------------------
            //                       method members
            // -------------------------------------------------------------
            public:

                /// Constructor without argument
                Recluster() {}

                /// Destructor
                virtual ~Recluster() {}

                //============================//
                //        Initialization      //
                //============================//
                // Initialize the parameters of the algorithm. Initialization includes multiple if conditions
                // Hence it would be optimum execution to initialize the algorithm during the initialisation
                // of the analysis

                // Constructor with arguments
                Recluster(Algorithm algorithm, MAfloat32 radius) { Initialize(algorithm, radius); }

                void Initialize(Algorithm algorithm, MAfloat32 radius) { SetJetDef(algorithm, radius); }

                //=======================//
                //        Execution      //
                //=======================//

                // Method to recluster a given jet. Returns only the hardest reclustered jet.
                const RecJetFormat* Execute(const RecJetFormat *jet)
                {
                    fastjet::contrib::Recluster recluster(*JetDefinition_);
                    fastjet::PseudoJet reclustered_jet = recluster(jet->pseudojet());
                    return __transform_jet(reclustered_jet);
                }

                // Method to recluster each jet in a given vector
                std::vector<const RecJetFormat *> Execute(std::vector<const RecJetFormat *> &jets)
                {
                    std::vector<const RecJetFormat *> output_jets;
                    for (auto &jet: jets)
                        output_jets.push_back(Execute(jet));

                    std::sort(
                        output_jets.begin(),
                        output_jets.end(),
                        [](const RecJetFormat *j1, const RecJetFormat *j2)
                        {
                            return (j1->pt() > j2->pt());
                        }
                    );

                    return output_jets;
                }

                //=============================//
                //        NOT IMPLEMENTED      //
                //=============================//

                void Execute(const EventFormat& event, std::string JetID)
                {
                    try { throw EXCEPTION_ERROR("This method has not been implemented", "", 1); }
                    catch (const std::exception& err) {
                        MANAGE_EXCEPTION(err);
                    }
                }

                template<class Func>
                std::vector<const RecJetFormat *> Execute(const RecJetFormat *jet, Func func)
                {
                    try { throw EXCEPTION_ERROR("This method has not been implemented", "", 1); }
                    catch (const std::exception& err) {
                        MANAGE_EXCEPTION(err);
                        return std::vector<const RecJetFormat *>();
                    }
                }
        };
    }
}

#endif //MADANALYSIS5_RECLUSTER_H
